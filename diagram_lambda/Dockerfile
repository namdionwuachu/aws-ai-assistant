FROM public.ecr.aws/lambda/python:3.9

RUN yum install -y graphviz

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

CMD ["app.lambda_handler"]
