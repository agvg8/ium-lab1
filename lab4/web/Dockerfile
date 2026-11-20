# Zadanie 4: statyczna strona serwowana przez wbudowany serwer HTTP Pythona
FROM python:3.11-slim

WORKDIR /site

# Kopiujemy tylko plik strony
COPY index.html .

# Dokumentacja portu, na którym nasłuchuje serwer (samo EXPOSE niczego nie udostępnia)
EXPOSE 8080

# Serwer HTTP wystawiający bieżący katalog (/site) na porcie 8080
CMD ["python", "-m", "http.server", "8080", "--bind", "0.0.0.0"]
