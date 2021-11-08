# FROM python:3.7-slim
FROM registry.access.redhat.com/ubi8/python-38
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD exec python -u manage.py runserver 0.0.0.0:8080
