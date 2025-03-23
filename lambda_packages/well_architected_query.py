import json
import boto3

def lambda_handler(event, context):
    client = boto3.client("bedrock-runtime")
    query = event["queryStringParameters"].get("query")
    body = json.dumps({"prompt": query, "maxTokens": 512})

    response = client.invoke_model(
        modelId="ai21.j2-grande-instruct",
        contentType="application/json",
        accept="application/json",
        body=body
    )

    result = json.loads(response["body"].read())
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"response": result["completions"][0]["data"]["text"]})
    }
