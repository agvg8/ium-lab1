import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# "or" obsługuje też pustą zmienną (GREETING=)
GREETING = os.getenv("GREETING") or "Hello z kodu (wartość domyślna w app.py)"
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "/data"))
PORT = os.getenv("PORT")


def save_message(message: str) -> Path:
    """Zapisuje wiadomość do OUTPUT_DIR/wynik.txt i zwraca ścieżkę pliku."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "wynik.txt"
    path.write_text(f"{message}\n", encoding="utf-8")
    return path


class GreetingHandler(BaseHTTPRequestHandler):
    """Na każde żądanie GET odpowiada wiadomością z GREETING."""

    def do_GET(self):
        body = f"{GREETING}\n".encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {GREETING}", flush=True)

    path = save_message(GREETING)
    print(f"Zapisano wiadomość do {path}", flush=True)

    if PORT:
        print(f"Serwer HTTP nasłuchuje na porcie {PORT} (Ctrl+C / docker stop kończy)", flush=True)
        HTTPServer(("0.0.0.0", int(PORT)), GreetingHandler).serve_forever()


if __name__ == "__main__":
    main()
