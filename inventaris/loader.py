"""Modul pembaca data: membaca CSV/JSON lalu memvalidasi tiap baris."""

import csv
import json
from pathlib import Path

from .exceptions import DataTidakValidError, FormatFileError

KOLOM_WAJIB = ("id_barang", "nama", "kategori", "jumlah", "harga", "lokasi", "kondisi")


def validasi_baris(baris, nomor):
    """Validasi satu baris data.

    Parameter:
        baris (dict): data mentah satu barang (nilai masih berupa string).
        nomor (int): nomor baris di file, untuk pesan error.
    Return:
        dict: baris bersih (jumlah -> int, harga -> int, teks di-strip).
    Raises:
        DataTidakValidError: jika kolom kosong, atau angka tidak valid/negatif.
    """
    kosong = [k for k in KOLOM_WAJIB if not str(baris.get(k, "")).strip()]
    if kosong:
        raise DataTidakValidError(f"baris {nomor}: kolom kosong {kosong}")

    try:
        jumlah = int(str(baris["jumlah"]).strip())
        harga = int(str(baris["harga"]).strip())
    except ValueError:
        raise DataTidakValidError(
            f"baris {nomor}: jumlah/harga bukan angka "
            f"(jumlah={baris['jumlah']!r}, harga={baris['harga']!r})"
        ) from None

    if jumlah < 0 or harga < 0:
        raise DataTidakValidError(f"baris {nomor}: jumlah/harga tidak boleh negatif")

    bersih = {k: str(baris[k]).strip() for k in KOLOM_WAJIB}
    bersih["jumlah"] = jumlah
    bersih["harga"] = harga
    return bersih


def _baca_mentah_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        pembaca = csv.DictReader(f)
        if pembaca.fieldnames is None:
            raise FormatFileError(f"File kosong: {path}")
        hilang = [k for k in KOLOM_WAJIB if k not in pembaca.fieldnames]
        if hilang:
            raise FormatFileError(f"Header CSV kurang kolom: {hilang}")
        return list(pembaca)


def _baca_mentah_json(path):
    with open(path, encoding="utf-8") as f:
        try:
            isi = json.load(f)
        except json.JSONDecodeError as e:
            raise FormatFileError(f"JSON rusak di {path}: {e}") from e
    if not isinstance(isi, list):
        raise FormatFileError("JSON harus berupa list of object")
    return isi


def baca_data(path):
    """Baca file CSV/JSON dan pisahkan baris valid dari baris bermasalah.

    Parameter:
        path (str | Path): lokasi file input (.csv atau .json).
    Return:
        tuple[list[dict], list[str]]: (data_valid, daftar_pesan_error).
    Raises:
        FormatFileError: file tidak ada / format tidak didukung / header salah.
    """
    path = Path(path)
    if not path.is_file():
        raise FormatFileError(f"File tidak ditemukan: {path}")

    ekstensi = path.suffix.lower()
    if ekstensi == ".csv":
        mentah = _baca_mentah_csv(path)
    elif ekstensi == ".json":
        mentah = _baca_mentah_json(path)
    else:
        raise FormatFileError(f"Ekstensi {ekstensi!r} tidak didukung (pakai .csv/.json)")

    valid, galat = [], []
    for nomor, baris in enumerate(mentah, start=2):  # baris 1 = header
        try:
            valid.append(validasi_baris(baris, nomor))
        except DataTidakValidError as e:
            galat.append(str(e))
    return valid, galat
