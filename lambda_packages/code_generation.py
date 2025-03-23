import json
import boto3
import requests

def lambda_handler(event, context):
    secrets = boto3.client("secretsmanager")
    secret = secrets.get_secret_value(SecretId="huggingface-api-key")
    HUGGING_FACE_KEY = json.loads(secret["SecretString"])

    query = event["queryStringParameters"].get("query")
    language = event["queryStringParameters"].get("language", "python")

    headers = {"Authorization": f"Bearer {HUGGING_FACE_KEY}"}
    response = requests.post(
        "https://api-inference.huggingface.co/models/bigcode/starcoder",
        headers=headers,
        json={"inputs": f"Write {language} code for: {query}"}
    )

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"code": response.json()[0]["generated_text"]})
    }
