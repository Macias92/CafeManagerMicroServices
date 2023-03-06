# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get -y install gettext
WORKDIR /code
COPY requirements.txt /code/
COPY django_cm_ms_auth-0.1.tar.gz /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install django_cm_ms_auth-0.1.tar.gz
COPY . /code/
