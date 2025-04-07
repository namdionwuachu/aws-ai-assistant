FROM public.ecr.aws/lambda/python:3.11

# Install system dependencies
RUN yum install -y gcc git swig && yum clean all

# Set pip and HF env vars
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=300 \
    PIP_PROGRESS_BAR=off \
    TRANSFORMERS_CACHE=/tmp/transformers_cache \
    HF_HOME=/tmp/hf_home

# Create writable cache dirs
RUN mkdir -p /tmp/transformers_cache /tmp/hf_home && \
    chmod 777 /tmp/transformers_cache /tmp/hf_home

# Copy and install Python dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip setuptools wheel \
 && python3 -m pip install --upgrade -r requirements.txt --target /var/task

# ✅ Pre-test critical modules
RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2'); print('✅ sentence-transformers loaded')"
RUN python3 -c "import faiss; print('✅ faiss imported')"

# Copy application code
COPY well_architected_query.py .

# Lambda entrypoint
CMD ["well_architected_query.lambda_handler"]

