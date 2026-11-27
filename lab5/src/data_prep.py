"""
Zadanie 1 – przygotowanie danych.

Funkcje load_data() i split_data() są czyste: nic nie wypisują i nic nie zapisują,
więc można je importować i testować niezależnie od reszty pipeline'u.
Pobranie surowego zbioru do CSV (efekt uboczny) jest wydzielone do osobnej funkcji
download_data(), wywoływanej tylko przy uruchomieniu modułu jako skryptu.
"""
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

import config


def load_data(path) -> pd.DataFrame:
    """Wczytuje zbiór danych z pliku CSV i zwraca DataFrame."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Nie znaleziono pliku {path}. Uruchom najpierw: python src/data_prep.py"
        )
    return pd.read_csv(path)


def split_data(df: pd.DataFrame, test_size: float, seed: int, target: str = config.TARGET_COLUMN):
    """
    Dzieli DataFrame na zbiór treningowy i testowy (ze stratyfikacją klas).

    Zwraca krotkę (X_train, X_test, y_train, y_test).
    Zgłasza ValueError dla pustego zbioru, braku kolumny docelowej
    lub test_size spoza przedziału (0, 1).
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df musi być obiektem pandas.DataFrame")
    if df.empty:
        raise ValueError("Zbiór danych jest pusty")
    if target not in df.columns:
        raise ValueError(f"Brak kolumny docelowej '{target}' w danych")
    if not 0 < test_size < 1:
        raise ValueError("test_size musi być liczbą z przedziału (0, 1)")

    X = df.drop(columns=[target])
    y = df[target]
    return train_test_split(X, y, test_size=test_size, random_state=seed, stratify=y)


def download_data(path) -> Path:
    """Zapisuje zbiór Wine (scikit-learn) do pliku CSV – jedyna funkcja z efektem ubocznym."""
    path = Path(path)
    df = load_wine(as_frame=True).frame          # 13 cech + kolumna 'target'
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


if __name__ == "__main__":
    # python src/data_prep.py – pobiera dane i pokazuje podstawowe informacje
    saved = download_data(config.DATA_PATH)
    df = load_data(saved)
    X_train, X_test, y_train, y_test = split_data(df, config.TEST_SIZE, config.RANDOM_SEED)
    print(f"Zapisano dane do {saved}")
    print(f"Rozmiar zbioru: {df.shape}")
    print(f"Zbiór treningowy: {len(X_train)} próbek, testowy: {len(X_test)} próbek")
