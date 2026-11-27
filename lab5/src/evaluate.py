"""
Zadanie 3 – ewaluacja modelu.

Wczytuje zapisany model z models/ (joblib) i dane testowe z data_prep.py,
liczy accuracy i classification_report, zapisuje wynik do pliku z .env (RESULTS_PATH).
Nie trenuje modelu ponownie. Uruchomienie: python src/evaluate.py
"""
import joblib
from sklearn.metrics import accuracy_score, classification_report

import config
from data_prep import load_data, split_data


def main() -> None:
    if not config.MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Brak modelu {config.MODEL_PATH}. Uruchom najpierw: python src/train.py"
        )
    model = joblib.load(config.MODEL_PATH)

    # Ten sam podział (ten sam TEST_SIZE i RANDOM_SEED) co w train.py,
    # więc model jest oceniany na danych, których nie widział podczas treningu
    df = load_data(config.DATA_PATH)
    _, X_test, _, y_test = split_data(df, config.TEST_SIZE, config.RANDOM_SEED)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    summary = (
        f"Model: {config.MODEL_TYPE} ({config.MODEL_PATH.name})\n"
        f"Zbiór testowy: {len(X_test)} próbek\n"
        f"Accuracy: {acc:.4f}\n\n"
        f"Classification report:\n{report}"
    )
    print(summary)
    config.RESULTS_PATH.write_text(summary, encoding="utf-8")
    print(f"Wyniki zapisano do {config.RESULTS_PATH}")


if __name__ == "__main__":
    main()
