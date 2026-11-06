"""
Wspólna konfiguracja projektu – wczytywana z pliku .env (python-dotenv).

Każdy moduł (data_prep, train, evaluate) importuje ten plik na samym początku,
więc parametry są zdefiniowane w jednym miejscu i żaden z nich nie jest
wpisany na sztywno w kodzie. Brak klucza w .env kończy się czytelnym błędem.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Katalog główny projektu (rodzic folderu src/) – ścieżki z .env liczone są względem niego,
# więc skrypty działają niezależnie od katalogu, z którego zostały uruchomione.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def _get(key: str) -> str:
    """Zwraca wartość zmiennej z .env albo zgłasza błąd, jeśli jej brakuje."""
    value = os.getenv(key)
    if value is None or value.strip() == "":
        raise RuntimeError(
            f"Brak zmiennej {key} w pliku .env – uzupełnij ją na podstawie .env.example"
        )
    return value.strip()


# --- Dane ---
DATA_PATH = PROJECT_ROOT / _get("DATA_PATH")
TARGET_COLUMN = _get("TARGET_COLUMN")
TEST_SIZE = float(_get("TEST_SIZE"))
RANDOM_SEED = int(_get("RANDOM_SEED"))

# --- Model i hiperparametry ---
MODEL_TYPE = _get("MODEL_TYPE")              # logistic_regression | random_forest
MAX_ITER = int(_get("MAX_ITER"))             # LogisticRegression
C = float(_get("C"))                         # LogisticRegression – siła regularyzacji
N_ESTIMATORS = int(_get("N_ESTIMATORS"))     # RandomForestClassifier

# --- Artefakty ---
MODEL_PATH = PROJECT_ROOT / _get("MODEL_PATH")
RESULTS_PATH = PROJECT_ROOT / _get("RESULTS_PATH")
