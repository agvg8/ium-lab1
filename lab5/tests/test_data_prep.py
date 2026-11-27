"""
Zadanie 5 – testy jednostkowe funkcji z data_prep.py.
Uruchomienie z katalogu głównego projektu: pytest -v
Testy działają na małym, sztucznym DataFrame – nie wymagają pliku z danymi.
"""
import pandas as pd
import pytest

from data_prep import load_data, split_data

TARGET = "target"


@pytest.fixture
def sample_df():
    """100 wierszy, 2 cechy, 2 zbalansowane klasy."""
    return pd.DataFrame({
        "f1": range(100),
        "f2": [x * 0.5 for x in range(100)],
        TARGET: [0, 1] * 50,
    })


def test_split_returns_four_parts(sample_df):
    result = split_data(sample_df, test_size=0.2, seed=42, target=TARGET)
    assert isinstance(result, (tuple, list))
    assert len(result) == 4


def test_split_test_size_proportion(sample_df):
    _, X_test, _, y_test = split_data(sample_df, test_size=0.2, seed=42, target=TARGET)
    assert len(X_test) == pytest.approx(len(sample_df) * 0.2, abs=1)
    assert len(y_test) == len(X_test)


def test_split_sizes_sum_to_total(sample_df):
    X_train, X_test, y_train, y_test = split_data(sample_df, test_size=0.3, seed=42, target=TARGET)
    assert len(X_train) + len(X_test) == len(sample_df)
    assert len(y_train) + len(y_test) == len(sample_df)


def test_split_removes_target_from_features(sample_df):
    X_train, X_test, _, _ = split_data(sample_df, test_size=0.2, seed=42, target=TARGET)
    assert TARGET not in X_train.columns
    assert TARGET not in X_test.columns


def test_split_is_reproducible(sample_df):
    a = split_data(sample_df, test_size=0.2, seed=42, target=TARGET)
    b = split_data(sample_df, test_size=0.2, seed=42, target=TARGET)
    assert a[1].index.equals(b[1].index)


def test_split_empty_dataframe_raises():
    empty = pd.DataFrame(columns=["f1", TARGET])
    with pytest.raises(ValueError):
        split_data(empty, test_size=0.2, seed=42, target=TARGET)


def test_split_missing_target_raises(sample_df):
    with pytest.raises(ValueError):
        split_data(sample_df.drop(columns=[TARGET]), test_size=0.2, seed=42, target=TARGET)


@pytest.mark.parametrize("bad_size", [0, 1, -0.1, 1.5])
def test_split_invalid_test_size_raises(sample_df, bad_size):
    with pytest.raises(ValueError):
        split_data(sample_df, test_size=bad_size, seed=42, target=TARGET)


def test_load_data_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_data(tmp_path / "nie_ma_takiego_pliku.csv")


def test_load_data_returns_dataframe(tmp_path, sample_df):
    path = tmp_path / "dane.csv"
    sample_df.to_csv(path, index=False)
    df = load_data(path)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == sample_df.shape
