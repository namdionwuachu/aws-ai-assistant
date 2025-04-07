import os
import json
import boto3
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate

# Read from environment variables (no defaults)
BUCKET = os.environ["VECTOR_BUCKET"]
INDEX_PREFIX = os.environ["VECTOR_PREFIX"]
INDEX_LOCAL_PATH = "/tmp/wellarch_index"

PROMPT_TEMPLATE = """Use the following AWS Well-Architected documentation to answer the question.

{context}

Question: {question}
Answer:"""

def download_index_from_s3():
    s3 = boto3.client("s3")
    os.makedirs(INDEX_LOCAL_PATH, exist_ok=True)
    for file_name in ["index.faiss", "index.pkl"]:
        s3.download_file(BUCKET, f"{INDEX_PREFIX}/{file_name}", f"{INDEX_LOCAL_PATH}/{file_name}")

def lambda_handler(event, context):
    try:
        query = event.get("queryStringParameters", {}).get("query")
        if not query:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing query"})}

        if not os.path.exists(f"{INDEX_LOCAL_PATH}/index.faiss"):
            download_index_from_s3()

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(INDEX_LOCAL_PATH, embeddings)

        docs = vectorstore.similarity_search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        sources = [doc.metadata.get("source", "") for doc in docs]

        prompt = PROMPT_TEMPLATE.format(context=context, question=query)

        client = boto3.client("bedrock-runtime")
        body = json.dumps({
            "prompt": prompt,
            "maxTokens": 512,
            "temperature": 0.7,
            "numResults": 1
        })

        response = client.invoke_model(
            modelId="ai21.j2-grande-instruct",
            contentType="application/json",
            accept="application/json",
            body=body
        )

        result = json.loads(response["body"].read())
        answer = result["completions"][0]["data"]["text"]

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "response": answer.strip(),
                "sources": sources
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

