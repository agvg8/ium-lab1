"""
Zadanie 2 – trening modelu.

Wczytuje dane funkcjami z data_prep.py, buduje Pipeline (StandardScaler + klasyfikator),
trenuje go na zbiorze treningowym i zapisuje do models/ w formacie .joblib.
Uruchomienie: python src/train.py
"""
import time

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import config
from data_prep import download_data, load_data, split_data


def build_model() -> Pipeline:
    """Tworzy Pipeline: standaryzacja cech + klasyfikator wybrany w .env (MODEL_TYPE)."""
    if config.MODEL_TYPE == "logistic_regression":
        clf = LogisticRegression(max_iter=config.MAX_ITER, C=config.C, random_state=config.RANDOM_SEED)
    elif config.MODEL_TYPE == "random_forest":
        clf = RandomForestClassifier(n_estimators=config.N_ESTIMATORS, random_state=config.RANDOM_SEED)
    else:
        raise ValueError(f"Nieznany MODEL_TYPE: {config.MODEL_TYPE}")
    return Pipeline([("scaler", StandardScaler()), ("clf", clf)])


def main() -> None:
    # Jeśli danych jeszcze nie ma (np. świeży klon repo w CI), pobieramy je
    if not config.DATA_PATH.exists():
        download_data(config.DATA_PATH)

    df = load_data(config.DATA_PATH)
    X_train, X_test, y_train, y_test = split_data(df, config.TEST_SIZE, config.RANDOM_SEED)

    model = build_model()
    start = time.perf_counter()
    model.fit(X_train, y_train)
    elapsed = time.perf_counter() - start

    config.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, config.MODEL_PATH)

    print(f"Model: {config.MODEL_TYPE}")
    print(f"Zbiór treningowy: {len(X_train)} próbek")
    print(f"Czas trenowania: {elapsed * 1000:.1f} ms")
    print(f"Accuracy na zbiorze treningowym: {model.score(X_train, y_train):.4f}")
    print(f"Zapisano model do {config.MODEL_PATH}")


if __name__ == "__main__":
    main()
