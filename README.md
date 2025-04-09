# 🧠 AWS Solution Architect AI Assistant

An intelligent assistant powered by AWS Lambda, Amazon Bedrock, and FAISS to help solution architects answer questions using the Well-Architected Framework and other AWS reference materials.

---

## 🚀 Features

- 📄 Retrieves insights from AWS PDFs (Well-Architected Framework, whitepapers, etc.)
- ⚙️ Serverless backend using AWS Lambda (Python)
- 🧠 Retrieval-Augmented Generation (RAG) using FAISS
- 🖼️ Auto-generates AWS architecture diagrams using Diagrams + Graphviz
- 🌐 Optional frontend for querying the assistant

---

## 📁 Project Structure

```plaintext
aws-solution-architect-ai-assistant/
│
├── README.md                      # Project overview and setup instructions
├── ai-assistant.yaml             # CloudFormation or CDK-generated deployment template
├── requirements.txt              # Python dependencies
├── test-event.json               # Sample input for Lambda test
├── response.json                 # Example response from the assistant
├── venv/                         # Local Python virtual environment
│
├── pdfs/                         # Source documents (e.g., AWS whitepapers, frameworks)
│   └── wellarchitected_framework.pdf
│
├── wellarch_index/               # FAISS index files for fast retrieval
│   ├── index.faiss
│   └── index.pkl
│
├── code_lambda/                  # General-purpose Lambda code
│   └── code_generation.py        # Builds FAISS index from PDFs
│
├── lambda_well_arch/             # Main Lambda for Well-Architected Q&A
│   ├── app.py                    # Lambda entry point
│   └── utils.py                  # Helper functions for FAISS, embeddings, etc.
│
├── diagram_lambda/               # Lambda to generate AWS architecture diagrams
│   └── generate_diagram.py
│
└── frontend/                     # Optional web-based UI to interact with assistant
    ├── index.html
    └── app.js
🛠️ Setup

1. Set up a virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Build FAISS Index
python code_lambda/code_generation.py
This will:

Read PDF files from pdfs/
Use Sentence Transformers to create embeddings
Save FAISS index in wellarch_index/
3. Deploy Lambda with CloudFormation
aws cloudformation deploy \
  --template-file ai-assistant.yaml \
  --stack-name ai-assistant-stack \
  --capabilities CAPABILITY_NAMED_IAM
Make sure required Lambda permissions and Bedrock access are set up properly.

4. Test the Lambda Locally
You can simulate a query with:

python lambda_well_arch/app.py
And use test-event.json to mock the input event.

💡 Future Enhancements

🔄 Vector store swap (e.g., OpenSearch, Pinecone)
🧠 Add more LLM agents (e.g., budgeting, compliance, migration)
📊 Visual analytics for query tracking
✨ Improved frontend with chat history and filters
👨‍💻 Author

Namdi Onwuachu — LinkedIn | Cloud AI Nexus

📄 License

MIT
