import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DATA_PATH = PROJECT_ROOT / os.getenv("DATA_PATH", "data/iris.csv")
TEST_SIZE = float(os.getenv("TEST_SIZE", 0.2))
RANDOM_SEED = int(os.getenv("RANDOM_SEED", 42))
RESULTS_PATH = PROJECT_ROOT / os.getenv("RESULTS_PATH", "wyniki.txt")


# --- Zadanie 3: wczytanie danych ---
def load_data(path: Path) -> pd.DataFrame:
    """Jeśli CSV nie istnieje, tworzy go z load_iris(); następnie wczytuje go do DataFrame."""
    if not path.exists():
        iris = load_iris(as_frame=True)
        df = iris.frame                                   # cechy + kolumna 'target'
        df["species"] = df["target"].map(dict(enumerate(iris.target_names)))
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
        print(f"Zapisano zbiór danych do {path}")
    return pd.read_csv(path)


def explore(df: pd.DataFrame) -> None:
    """Podstawowa eksploracja zbioru."""
    print("=== Pierwsze wiersze ===")
    print(df.head())
    print("\n=== Rozmiar zbioru (wiersze, kolumny) ===")
    print(df.shape)
    print("\n=== Statystyki opisowe ===")
    print(df.describe())


def main() -> None:
    df = load_data(DATA_PATH)
    explore(df)

    # --- Zadanie 4: podział danych i trening ---
    X = df.drop(columns=["target", "species"])            # cechy
    y = df["species"]                                     # etykiety

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=y,          # zachowuje proporcje klas w obu zbiorach
    )

    model = LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)
    model.fit(X_train, y_train)

    # --- Zadanie 5: ocena modelu ---
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    summary = (
        f"Model: LogisticRegression\n"
        f"Zbiór treningowy: {len(X_train)} próbek, testowy: {len(X_test)} próbek\n"
        f"Accuracy: {acc:.4f}\n\n"
        f"Classification report:\n{report}"
    )
    print("\n" + summary)
    RESULTS_PATH.write_text(summary, encoding="utf-8")
    print(f"Wyniki zapisano do {RESULTS_PATH}")


if __name__ == "__main__":
    main()