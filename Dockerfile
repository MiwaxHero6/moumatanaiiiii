# Dockerfile
FROM python:3.12

RUN apt-get update -y && \
	apt install -y wget make

RUN pip install --upgrade pip

WORKDIR /app

COPY ./ ./

RUN pip install --requirement requirements.txt

EXPOSE 8888
