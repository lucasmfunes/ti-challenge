# Set python version
ARG BASE_CONTAINER=python:3.8

# Set the base image 
FROM --platform=linux/amd64 $BASE_CONTAINER

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

USER root
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*


WORKDIR /loader-app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


COPY ./app ./app

CMD ["python", "-m", "app"]
