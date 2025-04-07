import json
import boto3
import requests
import re

def lambda_handler(event, context):
    # Initialize the Secrets Manager client
    secrets_client = boto3.client("secretsmanager")
    
    # Retrieve the secret value
    try:
        secret_response = secrets_client.get_secret_value(SecretId="AIAssistant/HuggingFaceKey")
        secret = json.loads(secret_response["SecretString"])
        hugging_face_key = secret["HUGGING_FACE_KEY"]
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": f"Error retrieving secret: {str(e)}"}, indent=2)
        }
    
    # Safely extract query parameters
    query_string_parameters = event.get("queryStringParameters") or {}
    query = query_string_parameters.get("query")
    language = query_string_parameters.get("language", "python")
    
    if not query:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Query parameter 'query' is required."}, indent=2)
        }
    
    # Prepare the request to the Hugging Face API
    headers = {"Authorization": f"Bearer {hugging_face_key}"}
    
    # Create a more focused prompt
    improved_prompt = f"""
    Write {language} code for: {query}
    
    - Include necessary imports
    - Use clear variable names
    - Add comments explaining complex logic
    - Follow best practices
    - Make the code complete and executable
    - Do not include explanatory text outside the code
    """
    
    payload = {"inputs": improved_prompt}
    
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/bigcode/starcoder",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        response_data = response.json()
        
        if isinstance(response_data, list) and response_data and "generated_text" in response_data[0]:
            generated_code = response_data[0]["generated_text"]
            # Clean up the generated code
            cleaned_code = clean_generated_code(generated_code, language)
        else:
            cleaned_code = "No code generated or unexpected response format."
            
    except requests.exceptions.RequestException as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": f"Error calling Hugging Face API: {str(e)}"}, indent=2)
        }
    
    # Return the cleaned code with pretty-printed JSON
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "code": cleaned_code,
            "language": language,
            "query": query
        }, indent=2)
    }

def clean_generated_code(code, language):
    """
    Clean up the generated code by removing explanatory text and formatting it properly.
    """
    # Remove the initial prompt that gets echoed in the response
    code = re.sub(r'^Write\s+\w+\s+code\s+for:.*?\n', '', code, flags=re.DOTALL)
    
    # Try to find actual code blocks
    if language.lower() == "python":
        # Look for Python code patterns
        code_blocks = re.findall(r'(?:^|\n)(?:import|from|def|class|if\s+__name__|#.*?|""".*?""").*?(?=\Z|\n\n\n)', code, re.DOTALL)
        if code_blocks:
            return "\n".join(code_blocks)
    
    # For other languages or if pattern matching fails, just return the cleaned text
    # Remove excessive newlines and spaces
    code = re.sub(r'\n{3,}', '\n\n', code)
    code = re.sub(r'\s+$', '', code, flags=re.MULTILINE)
    
    return code.strip()
