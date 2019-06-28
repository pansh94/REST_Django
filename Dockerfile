FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /django_code_rest
WORKDIR /django_code_rest
COPY requirements.txt /django_code_rest/
RUN pip install -r requirements.txt
COPY . /django_code_rest/
