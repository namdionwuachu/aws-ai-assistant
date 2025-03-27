FROM public.ecr.aws/lambda/python:3.11

# Install system dependencies
RUN yum install -y gcc git swig

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir --prefer-binary -r requirements.txt

# Copy app code
COPY app.py .

# Set the Lambda handler
CMD ["app.lambda_handler"]

