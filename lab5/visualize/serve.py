"""
Lab 5 – usługa visualize.

Zadanie 6: przy starcie sprawdza dostępność usługi train PO JEJ NAZWIE z pliku compose
(http://train:5000/status) i czeka, aż trening się zakończy. depends_on pilnuje tylko
startu kontenera train, a nie tego, czy trening już się skończył.
Zadanie 4: następnie serwuje katalog /srv (results/ i models/) przez HTTP.
"""
import json
import os
import socket
import time
import urllib.error
import urllib.request
from datetime import datetime
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

TRAIN_URL = os.getenv("TRAIN_URL", "http://train:5000/status")
PORT = int(os.getenv("PORT", "8080"))
SERVE_DIR = os.getenv("SERVE_DIR", "/srv")
POLL_SECONDS = float(os.getenv("POLL_SECONDS", "2"))
MAX_WAIT_SECONDS = float(os.getenv("MAX_WAIT_SECONDS", "300"))


def log(msg: str) -> None:
    print(f"[visualize {datetime.now():%H:%M:%S}] {msg}", flush=True)


def wait_for_train() -> dict | None:
    """Odpytuje usługę train, dopóki nie zgłosi zakończenia treningu (albo upłynie limit czasu)."""
    host = urlparse(TRAIN_URL).hostname
    deadline = time.time() + MAX_WAIT_SECONDS
    while time.time() < deadline:
        try:
            ip = socket.gethostbyname(host)          # rozwiązanie nazwy usługi w sieci compose
            with urllib.request.urlopen(TRAIN_URL, timeout=3) as resp:
                status = json.loads(resp.read().decode("utf-8"))
            log(f"Usługa '{host}' widoczna pod adresem {ip}, status: {status.get('status')}"
                f" (etap: {status.get('stage')})")
            if status.get("status") in ("done", "failed"):
                return status
        except socket.gaierror:
            log(f"Nie można rozwiązać nazwy '{host}' – czekam...")
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            log(f"Usługa '{host}' jeszcze nie odpowiada ({e}) – czekam...")
        time.sleep(POLL_SECONDS)
    log("Przekroczono czas oczekiwania na usługę train")
    return None


def main() -> None:
    log(f"Sprawdzam dostępność usługi train: {TRAIN_URL}")
    status = wait_for_train()
    if status and status.get("status") == "done":
        log(f"Trening zakończony, accuracy = {status.get('accuracy')}")
    elif status:
        log(f"Trening zakończył się błędem: {status.get('error')}")

    handler = partial(SimpleHTTPRequestHandler, directory=SERVE_DIR)
    log(f"Serwuję katalog {SERVE_DIR} na porcie {PORT} (results/, models/)")
    HTTPServer(("0.0.0.0", PORT), handler).serve_forever()


if __name__ == "__main__":
    main()
