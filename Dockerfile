FROM python:3.12
LABEL authors="carbon"
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt