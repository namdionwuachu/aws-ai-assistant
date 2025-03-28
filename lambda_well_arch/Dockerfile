FROM public.ecr.aws/lambda/python:3.11

# Install system dependencies
RUN yum install -y gcc git swig

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --prefer-binary -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy app code (now renamed)
COPY well_architected_query.py .

# Set the Lambda handler
CMD ["well_architected_query.lambda_handler"]

