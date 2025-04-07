import sys
import os
import json
import boto3
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate

# Ensure Lambda includes /var/task for installed packages
if "/var/task" not in sys.path:
    sys.path.insert(0, "/var/task")

# Environment variables
BUCKET = os.environ["VECTOR_BUCKET"]
INDEX_PREFIX = os.environ["VECTOR_PREFIX"]
INDEX_LOCAL_PATH = "/tmp/wellarch_index"

# Prompt template
PROMPT_TEMPLATE = """You are an expert on the AWS Well-Architected Framework.

Using the documentation below, answer the user's question with the following format:

- **Summary**: A one-sentence high-level answer.
- **Details**: A more in-depth explanation.
- **Key Points**: A bullet list of important takeaways.
- **Source Insight**: Where this applies in the Well-Architected Framework.

Documentation:
{context}

Question: {question}
Answer:"""

def download_index_from_s3():
    """Download FAISS index files from S3 to local /tmp directory."""
    s3 = boto3.client("s3")
    os.makedirs(INDEX_LOCAL_PATH, exist_ok=True)
    for file_name in ["index.faiss", "index.pkl"]:
        s3.download_file(BUCKET, f"{INDEX_PREFIX}/{file_name}", f"{INDEX_LOCAL_PATH}/{file_name}")

def lambda_handler(event, context):
    try:
        print(f"Event received: {json.dumps(event)}")

        if isinstance(event, str):
            event = json.loads(event)
            print("Parsed event from string")

        query = event.get("query") or event.get("queryStringParameters", {}).get("query")
        if not query:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing query"})
            }

        print(f"Query: {query}")

        if not os.path.exists(f"{INDEX_LOCAL_PATH}/index.faiss"):
            try:
                print(f"Downloading index from S3 bucket: {BUCKET}, prefix: {INDEX_PREFIX}")
                download_index_from_s3()
                print(f"✅ Index downloaded successfully to {INDEX_LOCAL_PATH}")
            except Exception as e:
                print(f"❌ Error downloading index: {str(e)}")
                return {
                    "statusCode": 500,
                    "body": json.dumps({"error": f"Failed to download index: {str(e)}"})
                }

        try:
            print("🔄 Loading embedding model...")
            import sentence_transformers
            print(f"✅ sentence_transformers version: {sentence_transformers.__version__}")
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            print("✅ Embedding model loaded successfully")
        except ImportError as e:
            print(f"❌ Import error: {str(e)}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Could not import sentence_transformers. Error: {str(e)}"})
            }
        except Exception as e:
            print(f"❌ Embedding error: {str(e)}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Failed to load embeddings: {str(e)}"})
            }

        try:
            print("🔄 Loading FAISS vector store...")
            vectorstore = FAISS.load_local(
                INDEX_LOCAL_PATH,
                embeddings,
                allow_dangerous_deserialization=True
            )
            print("✅ Vector store loaded successfully")
        except Exception as e:
            print(f"❌ Vector store error: {str(e)}")
            return {
                "statusCode": 500,
                "body": json.dumps({"error": f"Failed to load FAISS index: {str(e)}"})
            }

        print("🔄 Performing similarity search...")
        docs = vectorstore.similarity_search(query, k=3)
        for i, doc in enumerate(docs):
            print(f"Doc {i+1} content: {doc.page_content[:300]}")

        context_text = "\n\n".join([doc.page_content for doc in docs])
        sources = [doc.metadata.get("source", "") for doc in docs]
        print(f"✅ Found {len(docs)} relevant documents")

        prompt = PROMPT_TEMPLATE.format(context=context_text, question=query)
        print("Generated Prompt:\n", prompt)

        print("🔄 Calling Bedrock Jamba-Instruct model...")
        client = boto3.client("bedrock-runtime")

        body = json.dumps({
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500
        })

        response = client.invoke_model(
            modelId="ai21.jamba-instruct-v1:0",
            contentType="application/json",
            accept="application/json",
            body=body
        )

        result = json.loads(response["body"].read())
        answer = result["choices"][0]["message"]["content"].strip()

        print("🧠 Final LLM Answer:\n", answer)

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "response": answer,
                "sources": sources
            })
        }

    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"❌ Unhandled error: {str(e)}")
        print(f"Traceback: {error_msg}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

