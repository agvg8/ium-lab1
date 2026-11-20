# Obraz bazowy: lekka wersja Pythona
FROM python:3.11-slim

# Katalog roboczy w obrazie (tworzony automatycznie)
WORKDIR /app

# Logi Pythona trafiają od razu do `docker logs` (bez buforowania)
ENV PYTHONUNBUFFERED=1

# Zadanie 2: domyślna wartość zmiennej GREETING (można ją nadpisać flagą -e)
ENV GREETING="Witaj z Dockerfile (ENV)"

# Kopiowanie zawartości katalogu aplikacji (pliki z .dockerignore są pomijane)
COPY . .

# Port używany, gdy aplikacja działa jako serwer (zmienna PORT) – tylko dokumentacja
EXPOSE 8000

# Domyślne polecenie przy starcie kontenera
CMD ["python", "app.py"]
