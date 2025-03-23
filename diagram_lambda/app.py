import os, boto3, json
from diagrams import Diagram
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito

s3 = boto3.client("s3")
bucket = os.environ["S3_BUCKET"]

def save_diagram():
    filepath = "/tmp/aws_architecture.png"
    with Diagram("Extended AWS Architecture", filename="/tmp/aws_architecture", show=False):
        user_auth = Cognito("User Login")
        frontend = Lambda("Frontend Logic")
        api = APIGateway("API Gateway")
        compute = Lambda("Lambda Logic")
        db = Dynamodb("NoSQL DB")
        logs = Cloudwatch("Monitoring")
        backup = S3("Object Storage")

        user_auth >> frontend >> api >> compute >> db
        compute >> logs
        db >> backup
    return filepath

def upload_to_s3(filepath):
    key = "diagrams/" + os.path.basename(filepath)
    s3.upload_file(filepath, bucket, key)
    return f"https://{bucket}.s3.amazonaws.com/{key}"

def lambda_handler(event, context):
    file = save_diagram()
    url = upload_to_s3(file)
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"diagram_url": url})
    }
