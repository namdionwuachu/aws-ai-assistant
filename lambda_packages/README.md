
AI Assistant Stack Deployment

This project deploys a complete AI Assistant solution using AWS CloudFormation, Lambda (both ZIP and Docker), API Gateway, and supporting AWS services.

📁 Project Structure

.
├── diagram_lambda/            # Docker-based Lambda: architecture diagram generator
├── frontend/                  # Streamlit UI for user interactions
├── lambda_packages/           # Lightweight ZIP Lambda (e.g. code_generation)
├── lambda_well_arch/          # Docker-based Lambda: well-architected RAG logic
├── pdfs/                      # Source documents (e.g. WAF PDFs) for ingestion
├── wellarch_index/            # FAISS vector store index used by well_arch Lambda
├── ai-assistant.yaml          # CloudFormation template
├── README.md                  # Project overview and deployment instructions
└── .gitignore                 # Git exclusions

✅ Features

1 ZIP-based Lambda function:

code-generation — generates code using HuggingFace API

2 Docker-based Lambda functions (ECR):

well-architected-query — answers Well-Architected Framework queries

generate-diagram — produces AWS architecture diagrams

Other features:

S3 bucket for Lambda ZIP packages and architecture diagram storage

REST API via API Gateway with CORS support

IAM roles with access to logs, S3, Bedrock, and Secrets Manager

🚀 Deployment Steps

1. Package the ZIP Lambda

cd lambda_packages
zip code_generation.zip code_generation.py
aws s3 cp code_generation.zip s3://<your-bucket-name>/lambda/

2. Build & Push Docker Images

Well-Architected Query

cd lambda_well_arch
docker build -t well-architected-query .
docker tag well-architected-query:latest <account-id>.dkr.ecr.<region>.amazonaws.com/well-architected-query:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/well-architected-query:latest

Diagram Generator

cd diagram_lambda
docker build -t diagram-lambda .
docker tag diagram-lambda:latest <account-id>.dkr.ecr.<region>.amazonaws.com/diagram-lambda:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/diagram-lambda:latest

3. Deploy CloudFormation Stack

aws cloudformation deploy \
  --template-file ai-assistant.yaml \
  --stack-name AIAssistantStack \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    S3BucketName=<your-bucket-name> \
    WellArchitectedImageUri=<ecr-uri-for-well-architected> \
    DiagramLambdaImageUri=<ecr-uri-for-diagram-lambda>

🖥️ Streamlit Frontend

To run the frontend locally:

cd frontend
pip install -r requirements.txt
streamlit run app.py

🔧 Update app.py with your API Gateway URL

Replace this line:

endpoint = "https://<your-api-id>.execute-api.<region>.amazonaws.com/Prod/query"

With your actual API Gateway endpoint found in:

CloudFormation Outputs

API Gateway Console → Stages → Prod

🔍 Example API Test

curl -X PUT "https://<your-api-id>.execute-api.<region>.amazonaws.com/Prod/query?query=Draw EC2 > S3 > RDS"

📬 Questions?

Open an issue or reach out — happy to help. Happy building! 🚀

📝 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute it. A copy of the license is included in the repository.
