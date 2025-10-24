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

        # 2. Create a private S3 bucket for the frontend static site
        frontend_bucket = s3.Bucket(
            self,
            f"{APP_NAME}-FrontendBucket",
            bucket_name=f"{APP_NAME.lower()}-{ACCOUNT}-{REGION}",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL, # Keep the bucket private
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # 3. Create a CloudFront Origin Access Identity (OAI)
        oai = cloudfront.OriginAccessIdentity(
            self, f"{APP_NAME}-OAI"
        )
        frontend_bucket.grant_read(oai)

        # 4. Create a CloudFront distribution pointing to the private S3 bucket via OAI
        distribution = cloudfront.Distribution(
            self,
            f"{APP_NAME}-CloudFrontDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(frontend_bucket, origin_access_identity=oai)
            ),
            default_root_object="index.html",
        )

        # 5. Deploy the built frontend to the S3 bucket
        s3_deployment.BucketDeployment(
            self,
            f"{APP_NAME}-S3Deployment",
            sources=[s3_deployment.Source.asset(os.path.join(FRONTEND_PATH, "dist"))],
            destination_bucket=frontend_bucket,
            distribution=distribution,
            distribution_paths=["/*"],
        )

        # --- Backend Deployment (EC2 Instance) ---

        # 1. Define the VPC
        vpc = ec2.Vpc(self, f"{APP_NAME}-Vpc", max_azs=2)

        # 2. Build and push the Docker image to ECR
        backend_image = ecr_assets.DockerImageAsset(
            self, f"{APP_NAME}-BackendImage", directory=DOCKERFILE_PATH
        )

        # 3. Create an IAM role for the EC2 instance
        ec2_role = iam.Role(
            self, f"{APP_NAME}-EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )
        backend_image.repository.grant_pull(ec2_role)
        ec2_role.add_to_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel"],
                resources=[f"arn:aws:bedrock:{self.region}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"],
            )
        )

        # 4. Create the EC2 instance with an SSH key pair
        instance = ec2.Instance(
            self,
            f"{APP_NAME}-Instance",
            vpc=vpc,
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            role=ec2_role,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            key_name="aws-agetic-ai-key", # CRITICAL: Assumes you created this key pair
        )

        # 5. Create an Elastic IP and associate it with the instance
        eip = ec2.CfnEIP(self, f"{APP_NAME}-EIP")
        ec2.CfnEIPAssociation(
            self,
            f"{APP_NAME}-EIPAssociation",
            eip=eip.ref,
            instance_id=instance.instance_id,
        )

        # 6. Add a simplified and corrected User Data script
        instance.user_data.add_commands(
            "exec > /home/ec2-user/user-data.log 2>&1",  # Log to a user-writable directory
            "set -x",  # Echo all commands to the log file
            "dnf update -y",
            "dnf install -y docker",
            "systemctl start docker",  # Correct command for Amazon Linux 2023
            "systemctl enable docker", # Ensure Docker starts on reboot
            "usermod -a -G docker ec2-user",
            f"aws ecr get-login-password --region {self.region} | docker login --username AWS --password-stdin {self.account}.dkr.ecr.{self.region}.amazonaws.com",
            f"docker pull {backend_image.image_uri}",
            f"docker run -d -p 80:8080 "
            f"-e AWS_REGION={self.region} "
            f"-e BEDROCK_MODEL_ID='anthropic.claude-3-sonnet-20240229-v1:0' "
            f"{backend_image.image_uri}",
        )

        # 7. Open ports for HTTP, HTTPS, and SSH
        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(80), "Allow HTTP In")
        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(443), "Allow HTTPS In")
        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(22), "Allow SSH In for debugging")

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
            value=f"http://{eip.ref}",
            description="The Public IP of the backend EC2 instance. Update .env.production with this.",
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
