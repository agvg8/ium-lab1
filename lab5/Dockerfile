# Lab 5 – obraz z pipeline'em z lab. 3 (data_prep -> train -> evaluate)
FROM python:3.11-slim

WORKDIR /app

# Logi Pythona trafiają od razu do docker logs / docker compose logs
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir uv \
 && uv pip install --system --no-cache -r requirements.txt

COPY . .

# Domyślne polecenie: trening modelu (w compose nadpisane pełnym pipeline'em)
CMD ["python", "src/train.py"]
