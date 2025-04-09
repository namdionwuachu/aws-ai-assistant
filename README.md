# 🧠 AWS Solution Architect AI Assistant

An intelligent assistant for AWS professionals, built with Bedrock-hosted LLMs, FAISS, and serverless infrastructure. It can answer AWS architecture questions, generate diagrams, and even write infrastructure code — all from natural language prompts.

---

## 🚀 Features

- 📄 **Ask AWS Architecture Questions**  
  Uses RAG (Retrieval-Augmented Generation) with Bedrock + FAISS to answer questions from AWS Well-Architected PDFs and whitepapers.

- ⚙️ **Generate Infrastructure Code**  
  Creates CloudFormation, CDK, or Terraform snippets based on your prompts (e.g., "Create a VPC with 2 subnets and a NAT Gateway").

- 🖼️ **Draw AWS Architecture Diagrams**  
  Auto-generates diagrams using the [Diagrams](https://diagrams.mingrammer.com/) library and Graphviz via Lambda.

- 🌐 **Minimal Frontend Interface**  
  Interact with the assistant via a simple web interface (optional).

---

## 📁 Project Structure

```plaintext
aws-solution-architect-ai-assistant/
│
├── README.md                      # Project overview and setup instructions
├── ai-assistant.yaml             # CloudFormation/CDK deployment template
├── test-event.json               # Sample input for Lambda testing
├── response.json                 # Example response from assistant
├── venv/                         # Python virtual environment
│
├── pdfs/                         # Source AWS reference materials
│   └── wellarchitected_framework.pdf
│
├── wellarch_index/               # FAISS vector index
│   ├── index.faiss
│   └── index.pkl
│
├── code_lambda/                  # Utility or supporting Lambda code
│   └── code_generation.py        # Code to create FAISS index from PDFs
│
├── lambda_well_arch/             # Main Lambda for Well-Architected Q&A (Bedrock + FAISS)
│   ├── Dockerfile                # Containerized Lambda deployment
│   ├── build_faiss_index.py      # Script to build FAISS index from PDFs
│   ├── input.json                # Example input for testing
│   ├── output.json               # Example output from inference
│   ├── response.json             # Sample Bedrock/FAISS response
│   ├── requirements.txt          # Python dependencies for the Lambda
│   └── well_architected_query.py # Lambda handler for answering queries
│
├── diagram_lambda/               # Lambda to auto-generate AWS architecture diagrams
│   ├── Dockerfile                # Containerized Lambda deployment
│   ├── app.py                    # Lambda handler to generate diagrams
│   ├── event.json                # Sample event input
│   ├── output.json               # Sample generated diagram metadata
│   └── requirements.txt          # Python dependencies for diagram generation
│
└── frontend/                     # Optional web-based UI
    ├── index.html
    └── app.js



🛠️ Setup Instructions

1. Create and Activate a Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install -r lambda_well_arch/requirements.txt
2. Build the FAISS Index from AWS PDFs
python lambda_well_arch/build_faiss_index.py
Loads PDFs from pdfs/
Embeds content with sentence-transformers
Saves index to wellarch_index/
3. Deploy Lambdas via CloudFormation
aws cloudformation deploy \
  --template-file ai-assistant.yaml \
  --stack-name ai-assistant-stack \
  --capabilities CAPABILITY_NAMED_IAM
Ensure your IAM roles allow:
Access to Amazon Bedrock
Access to S3 (if needed for index or logs)
4. Run Locally for Testing
Querying with Bedrock + FAISS:

python lambda_well_arch/well_architected_query.py
Diagram Generation:

python diagram_lambda/app.py
💬 Prompt Examples

Use natural language to access different functions:
💡 "What are the five pillars of the AWS Well-Architected Framework?"
🏗️ "Generate a CloudFormation template for an S3 bucket with encryption enabled."
🖼️ "Create an architecture diagram for a serverless web app with Lambda, API Gateway, and DynamoDB."
📦 "Explain how to optimize Athena queries over Parquet files in S3."
🔮 Future Enhancements

📊 Query history and analytics dashboard
🔐 Enhanced vector store with OpenSearch or Pinecone
🧠 Multi-agent support (e.g., compliance, cost optimization)
🌍 Multi-language or region-based personalization
🧪 Unit and integration testing framework
👨‍💻 Author

Namdi Onwuachu — LinkedIn | Cloud AI Nexus


