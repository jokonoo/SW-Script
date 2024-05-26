FROM python:3.11-alpine
LABEL authors="jokonoo"
ENV PYTHONBUFFERED True
ENV PYTHONPATH /app
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
