ARG BASE_CONTAINER=python:3.8

FROM --platform=linux/amd64 $BASE_CONTAINER

WORKDIR /extraction-app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .


CMD ["python", "-m", "app"]
