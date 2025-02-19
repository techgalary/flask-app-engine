# Use official Python image
FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD exec gunicorn --bind :$PORT main:app
