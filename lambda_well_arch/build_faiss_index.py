import os
import boto3
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Your bucket and prefix where PDFs are
BUCKET = "ai-aws-assistant"
PDF_PREFIX = "wafr/"
LOCAL_PDF_DIR = "pdfs/"
INDEX_DIR = "wellarch_index/"

os.makedirs(LOCAL_PDF_DIR, exist_ok=True)

# S3 client
s3 = boto3.client("s3")

# List all PDFs in the S3 folder
response = s3.list_objects_v2(Bucket=BUCKET, Prefix=PDF_PREFIX)
pdf_keys = [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".pdf")]

all_docs = []

# Download and process each PDF
for key in pdf_keys:
    filename = os.path.basename(key)
    local_path = os.path.join(LOCAL_PDF_DIR, filename)
    s3.download_file(BUCKET, key, local_path)

    loader = PyPDFLoader(local_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(pages)

    for chunk in chunks:
        chunk.metadata["source"] = key  # save source filename

    all_docs.extend(chunks)

print(f"✅ {len(pdf_keys)} PDFs → {len(all_docs)} text chunks")

# Embed with HuggingFace
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(all_docs, embeddings)

# Save locally
os.makedirs(INDEX_DIR, exist_ok=True)
vectorstore.save_local(INDEX_DIR)
print(f"✅ FAISS index saved to {INDEX_DIR}")
