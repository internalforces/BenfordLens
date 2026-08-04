import pytest

from benford_lens.io.csv_loader import CsvLoadError, load_csv


def test_loads_plain_utf8_csv(tmp_path):
    csv_path = tmp_path / "utf8.csv"
    csv_path.write_text("name,amount\nalice,120\nbob,45\n", encoding="utf-8")

    df = load_csv(str(csv_path))

    assert list(df.columns) == ["name", "amount"]
    assert df["amount"].tolist() == [120, 45]


def test_loads_utf8_sig_csv_with_bom(tmp_path):
    csv_path = tmp_path / "bom.csv"
    csv_path.write_text("name,amount\n김철수,1000\n", encoding="utf-8-sig")

    df = load_csv(str(csv_path))

    assert df["name"].tolist() == ["김철수"]


def test_loads_cp949_encoded_csv(tmp_path):
    csv_path = tmp_path / "cp949.csv"
    csv_path.write_bytes("name,amount\n박영희,500\n".encode("cp949"))

    df = load_csv(str(csv_path))

    assert df["name"].tolist() == ["박영희"]
    assert df["amount"].tolist() == [500]


def test_raises_csv_load_error_when_file_missing(tmp_path):
    missing_path = tmp_path / "does-not-exist.csv"

    with pytest.raises(CsvLoadError):
        load_csv(str(missing_path))
