#!/usr/bin/env python3
import os
import sys
import subprocess
import aws_cdk as cdk
from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_s3_assets as s3_assets,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_ecr_assets as ecr_assets,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_logs as logs,
    RemovalPolicy,
)
from constructs import Construct

# Configuration
APP_NAME = "aws-agetic-ai"
FRONTEND_PATH = "frontend"
DOCKERFILE_PATH = "."
ACCOUNT = os.environ.get("CDK_DEFAULT_ACCOUNT")
REGION = os.environ.get("CDK_DEFAULT_REGION")


def check_docker_running():
    """Checks if the Docker daemon is running."""
    try:
        subprocess.run("docker info", shell=True, check=True, capture_output=True)
        print("Docker daemon is running.")
        return True
    except subprocess.CalledProcessError:
        print("ERROR: Docker daemon is not running. Please start Docker and try again.")
        return False


class AgeticAiStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # --- Frontend Deployment (S3 + CloudFront) ---

        # 1. Build the frontend application
        print("Building frontend application...")
        try:
            subprocess.run(
                "npm ci && npm run build",
                shell=True,
                check=True,
                cwd=FRONTEND_PATH,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print("Frontend build successful.")
        except subprocess.CalledProcessError as e:
            print("ERROR: Frontend build failed.")
            print(e.stderr.decode())
            raise

        # 2. Create S3 bucket for the frontend static site
        frontend_bucket = s3.Bucket(
            self,
            f"{APP_NAME}-FrontendBucket",
            bucket_name=f"{APP_NAME.lower()}-{ACCOUNT}-{REGION}",
            website_index_document="index.html",
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(block_public_policy=False),
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # 3. Create a CloudFront distribution using the S3 bucket's website URL
        distribution = cloudfront.Distribution(
            self,
            f"{APP_NAME}-CloudFrontDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.HttpOrigin(frontend_bucket.bucket_website_domain_name)
            ),
            default_root_object="index.html",
        )

        # 4. Deploy the built frontend to the S3 bucket
        s3_deployment.BucketDeployment(
            self,
            f"{APP_NAME}-S3Deployment",
            sources=[s3_deployment.Source.asset(os.path.join(FRONTEND_PATH, "dist"))],
            destination_bucket=frontend_bucket,
            distribution=distribution,
            distribution_paths=["/*"],
        )

        # --- Backend Deployment (EC2 Instance) ---

        # 1. Create CloudWatch Log Groups
        container_log_group = logs.LogGroup(
            self,
            f"{APP_NAME}-BackendLogGroup",
            log_group_name=f"/aws/ec2/{APP_NAME}-backend",
            removal_policy=RemovalPolicy.DESTROY,
        )
        startup_log_group = logs.LogGroup(
            self,
            f"{APP_NAME}-StartupLogGroup",
            log_group_name=f"/aws/ec2/{APP_NAME}-startup-logs",
            removal_policy=RemovalPolicy.DESTROY,
        )

        # 2. Define the VPC
        vpc = ec2.Vpc(self, f"{APP_NAME}-Vpc", max_azs=2)

        # 3. Build and push the Docker image to ECR
        backend_image = ecr_assets.DockerImageAsset(
            self, f"{APP_NAME}-BackendImage", directory=DOCKERFILE_PATH
        )

        # 4. Create an IAM role for the EC2 instance
        ec2_role = iam.Role(
            self, f"{APP_NAME}-EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
            ]
        )
        backend_image.repository.grant_pull(ec2_role)
        container_log_group.grant_write(ec2_role)
        startup_log_group.grant_write(ec2_role)

        # Add policy to allow invoking Bedrock models
        ec2_role.add_to_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel"],
                resources=[f"arn:aws:bedrock:{self.region}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"],
            )
        )

        # 5. Create the EC2 instance
        instance = ec2.Instance(
            self,
            f"{APP_NAME}-Instance",
            vpc=vpc,
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            role=ec2_role,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        # 6. Create CloudWatch Agent config file content
        cw_agent_config = {
            "agent": {"run_as_user": "root"},
            "logs": {
                "logs_collected": {
                    "files": {
                        "collect_list": [
                            {
                                "file_path": "/var/log/user-data.log",
                                "log_group_name": startup_log_group.log_group_name,
                                "log_stream_name": "{instance_id}",
                            }
                        ]
                    }
                }
            },
        }

        import json
        cw_agent_config_json = json.dumps(cw_agent_config)

        # 7. Add User Data to install everything and send logs
        instance.user_data.add_commands(
            "exec > /var/log/user-data.log 2>&1", # Redirect all output
            "set -x", # Echo all commands

            "# Install CW Agent",
            "dnf install -y amazon-cloudwatch-agent",
            f"echo '{cw_agent_config_json}' > /opt/aws/amazon-cloudwatch-agent/bin/config.json",
            "amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s",

            "# Install Docker",
            "dnf install -y docker",
            "service docker start",
            "usermod -a -G docker ec2-user",

            "# Login to ECR",
            f"aws ecr get-login-password --region {self.region} | docker login --username AWS --password-stdin {self.account}.dkr.ecr.{self.region}.amazonaws.com",

            "# Run Container",
            f"docker pull {backend_image.image_uri}",
            f"docker run -d -p 80:8080 "
            f"--log-driver=awslogs "
            f"--log-opt awslogs-group={container_log_group.log_group_name} "
            f"--log-opt awslogs-region={self.region} "
            f"--log-opt awslogs-stream-prefix=container "
            f"-e AWS_REGION={self.region} "
            f"-e BEDROCK_MODEL_ID='anthropic.claude-3-sonnet-20240229-v1:0' "
            f"{backend_image.image_uri}",
        )

        # 8. Open port 80 to allow inbound HTTP traffic
        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Allow HTTP In")

        # --- Outputs ---
        cdk.CfnOutput(
            self,
            "CloudFrontURL",
            value=f"https://{distribution.distribution_domain_name}",
            description="The URL of the frontend application.",
        )
        cdk.CfnOutput(
            self,
            "EC2_Backend_URL",
            value=f"http://{instance.instance_public_ip}",
            description="The Public IP of the backend EC2 instance. Update .env.production with this.",
        )
        cdk.CfnOutput(
            self,
            "BackendContainerLogGroupName",
            value=container_log_group.log_group_name,
            description="CloudWatch Log Group name for the backend container.",
        )
        cdk.CfnOutput(
            self,
            "BackendStartupLogGroupName",
            value=startup_log_group.log_group_name,
            description="CloudWatch Log Group name for the EC2 startup script.",
        )


def main():
    """Initializes and synthesizes the CDK app."""
    print("Starting CDK deployment...")

    if not check_docker_running():
        sys.exit(1)

    if not all([ACCOUNT, REGION]):
        raise EnvironmentError(
            "CDK environment variables CDK_DEFAULT_ACCOUNT and CDK_DEFAULT_REGION must be set."
            "Please configure your AWS CLI and environment."
        )

    app = cdk.App()
    AgeticAiStack(app, APP_NAME)
    app.synth()


if __name__ == "__main__":
    main()
