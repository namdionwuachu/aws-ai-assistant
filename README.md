# AI Assistant Stack Deployment

This project deploys a complete AI Assistant solution using AWS CloudFormation, Lambda, API Gateway, and Docker containers.

## 📁 Project Structure

```
ai-assistant/
├── diagram_lambda/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── lambda_packages/
│   ├── well_architected_query.py
│   └── code_generation.py
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── ai-assistant.yaml
├── README.md
```

## ✅ Features

- 3 Lambda functions:
  - `well-architected-query` (ZIP)
  - `code-generation` (ZIP)
  - `generate-diagram` (Docker container)
- S3 bucket for:
  - Lambda packages
  - Generated architecture diagrams
- API Gateway with CORS
- IAM role with permissions for S3, logs, Secrets Manager, and Bedrock

---

## 🚀 Deployment Steps

### 1. Package Lambda Functions

```bash
cd lambda_packages
zip well_architected_query.zip well_architected_query.py
zip code_generation.zip code_generation.py

aws s3 cp well_architected_query.zip s3://<your-bucket-name>/lambda/
aws s3 cp code_generation.zip s3://<your-bucket-name>/lambda/
```

### 2. Build & Push Docker Image

```bash
cd diagram_lambda
docker build -t diagram-lambda .

aws ecr create-repository --repository-name diagram-lambda
aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com

docker tag diagram-lambda:latest <account-id>.dkr.ecr.<region>.amazonaws.com/diagram-lambda:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/diagram-lambda:latest
```

### 3. Deploy the Stack

```bash
aws cloudformation deploy \
  --template-file ai-assistant.yaml \
  --stack-name AIAssistantStack \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides S3BucketName=<your-bucket-name>
```

---

## 🖥️ Streamlit Frontend

To run the frontend locally:

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### 🔧 Update `app.py` with your API Gateway URL

Open `frontend/app.py` and replace this line:

```python
endpoint = "https://<your-api-id>.execute-api.<region>.amazonaws.com/Prod/query"
```

With your actual API Gateway endpoint from:
- CloudFormation Outputs
- API Gateway Console > Stages > Prod

---

## 🔍 Example API Test

```bash
curl -X PUT "https://<your-api-id>.execute-api.<region>.amazonaws.com/Prod/query?query=Draw EC2 > S3 > RDS"
```

---

## 📬 Questions?

Open an issue or reach out. Happy building! 🚀
