# Lab 5 – lekki serwer HTTP z wynikami treningu (tylko biblioteka standardowa Pythona)
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY serve.py .

# Port serwera – wystawiany na hosta w docker-compose.yml
EXPOSE 8080

CMD ["python", "serve.py"]
