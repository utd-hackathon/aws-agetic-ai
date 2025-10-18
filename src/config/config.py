import os
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AWSConfig:
    """AWS Configuration and client setup for the UTD Career Advisory AI System"""

    def __init__(self):
        """Initialize AWS configuration from environment variables"""
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.bedrock_model_id = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
        self.bedrock_endpoint = os.getenv("BEDROCK_ENDPOINT", "bedrock-runtime.us-east-1.amazonaws.com")

        # Validate required configuration
        self._validate_config()

    def _validate_config(self):
        """Validate that required AWS configuration is present"""
        required_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]
        missing = [var for var in required_vars if not os.getenv(var)]

        if missing:
            raise ValueError(f"Missing required AWS configuration: {', '.join(missing)}")

    def get_bedrock_client(self):
        """Get an AWS Bedrock runtime client"""
        return boto3.client(
            service_name="bedrock-runtime",
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            endpoint_url=self.bedrock_endpoint
        )

    def get_s3_client(self):
        """Get an AWS S3 client"""
        return boto3.client(
            service_name="s3",
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

    def get_dynamodb_client(self):
        """Get an AWS DynamoDB client"""
        return boto3.client(
            service_name="dynamodb",
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )

    def get_bedrock_agent_client(self):
        """Get an AWS Bedrock agent client"""
        return boto3.client(
            service_name="bedrock-agent",
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
