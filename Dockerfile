FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /project

COPY config/requirements.txt .

RUN python -m pip install -r requirements.txt
