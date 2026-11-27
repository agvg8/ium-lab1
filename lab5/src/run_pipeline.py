"""
Lab 5 – punkt startowy usługi train w Docker Compose.

1. Uruchamia mały serwer HTTP ze statusem (GET /status) na porcie STATUS_PORT,
   żeby inne usługi mogły sprawdzić stan treningu, odwołując się do nazwy usługi
   (np. http://train:5000/status).
2. Wykonuje kolejno etapy pipeline'u z lab. 3: data_prep.py -> train.py -> evaluate.py
   (każdy jako osobny proces, dokładnie tak jak przy uruchomieniu lokalnym).
3. Po zakończeniu zostawia serwer statusu włączony, aby usługa visualize mogła
   odczytać wynik. Gdy STATUS_PORT nie jest ustawiony, kończy działanie po pipeline.
"""
import json
import os
import subprocess
import sys
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
STAGES = ["data_prep.py", "train.py", "evaluate.py"]

# Wspólny stan pipeline'u, odczytywany przez serwer statusu
state = {"status": "starting", "stage": None, "started_at": datetime.now().isoformat(timespec="seconds")}


def log(msg: str) -> None:
    print(f"[train {datetime.now():%H:%M:%S}] {msg}", flush=True)


class StatusHandler(BaseHTTPRequestHandler):
    """GET /status zwraca JSON z aktualnym stanem pipeline'u."""

    def do_GET(self):
        if self.path.rstrip("/") != "/status":
            self.send_response(404)
            self.end_headers()
            return
        body = json.dumps(state, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Każde zapytanie ze strony innej usługi trafia do logów train
        log(f"zapytanie o status od {self.client_address[0]}: {fmt % args}")


def start_status_server(port: int) -> HTTPServer:
    server = HTTPServer(("0.0.0.0", port), StatusHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    log(f"Serwer statusu nasłuchuje na porcie {port} (GET /status)")
    return server


def run_stage(script: str) -> None:
    state.update(status="running", stage=script)
    log(f"=== Etap: {script} ===")
    subprocess.run([sys.executable, str(SRC_DIR / script)], check=True)


def read_accuracy() -> str | None:
    """Odczytuje accuracy z pliku wyników (RESULTS_PATH), jeśli istnieje."""
    try:
        from config import RESULTS_PATH
        for line in Path(RESULTS_PATH).read_text(encoding="utf-8").splitlines():
            if line.startswith("Accuracy:"):
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return None


def main() -> None:
    port = os.getenv("STATUS_PORT")
    server = start_status_server(int(port)) if port else None

    try:
        for script in STAGES:
            run_stage(script)
    except subprocess.CalledProcessError as e:
        state.update(status="failed", error=f"{e.cmd[-1]} zakończył się kodem {e.returncode}")
        log(f"BŁĄD: {state['error']}")
        if not server:
            sys.exit(1)
    else:
        state.update(status="done", stage=None, accuracy=read_accuracy(),
                     finished_at=datetime.now().isoformat(timespec="seconds"))
        log(f"Pipeline zakończony, accuracy = {state['accuracy']}")

    if server:
        log("Serwer statusu pozostaje włączony (docker compose down kończy usługę)")
        threading.Event().wait()


if __name__ == "__main__":
    main()
