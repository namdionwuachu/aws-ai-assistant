import os, boto3, json, uuid
from diagrams import Diagram
from diagrams.aws.compute import EC2, ECS, Lambda, Batch
from diagrams.aws.database import RDS, Dynamodb, Redshift, Neptune
from diagrams.aws.storage import S3, EFS
from diagrams.aws.network import VPC, ELB, Route53, CloudFront, APIGateway
from diagrams.aws.ml import Sagemaker, Rekognition, Comprehend
from diagrams.aws.security import IAM, Cognito, WAF, Shield
from diagrams.aws.management import Cloudwatch

# Initialize S3 client
s3 = boto3.client("s3")

# Service class map (not instances)
SERVICE_MAP = {
    "s3": S3,
    "efs": EFS,
    "lambda": Lambda,
    "ec2": EC2,
    "ecs": ECS,
    "batch": Batch,
    "dynamodb": Dynamodb,
    "rds": RDS,
    "redshift": Redshift,
    "neptune": Neptune,
    "vpc": VPC,
    "elb": ELB,
    "route53": Route53,
    "cloudfront": CloudFront,
    "apigateway": APIGateway,
    "sagemaker": Sagemaker,
    "rekognition": Rekognition,
    "comprehend": Comprehend,
    "iam": IAM,
    "cognito": Cognito,
    "waf": WAF,
    "shield": Shield,
    "cloudwatch": Cloudwatch
}

# Generate diagram from input
def save_diagram(service_input: str, title: str, filename: str):
    requested_services = [s.strip().lower() for s in service_input.split("+")]
    valid_services = [s for s in requested_services if s in SERVICE_MAP]

    if not valid_services:
        raise ValueError("No supported AWS services found.")

    with Diagram(title, filename=filename.replace(".png", ""), show=False):
        nodes = [SERVICE_MAP[s](s.upper()) for s in valid_services]
        for i in range(len(nodes) - 1):
            nodes[i] >> nodes[i + 1]

    return filename

# Upload diagram to S3 (no ACL override)
def upload_to_s3(filepath, bucket, key):
    s3.upload_file(filepath, bucket, key)
    return f"https://{bucket}.s3.amazonaws.com/{key}"

# Lambda handler
def lambda_handler(event, context):
    try:
        bucket = os.environ["S3_BUCKET"]
        title = event.get("title", "AWS Architecture")
        service_input = event.get("service") or "lambda + apigateway + cloudwatch"

        unique_id = str(uuid.uuid4())
        filename = f"/tmp/aws_diagram_{unique_id}.png"
        s3_key = f"diagrams/aws_diagram_{unique_id}.png"

        save_diagram(service_input, title, filename)
        url = upload_to_s3(filename, bucket, s3_key)

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"diagram_url": url})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

