# syntax=docker/dockerfile:1
FROM python:3.9-alpine
COPY requirements.txt .
RUN pip3 install -r requirements.txt
WORKDIR /app
#COPY .env .
COPY main.py .

EXPOSE 8000

#CMD ["source", ".env"]
CMD ["strawberry", "server", "main"]

