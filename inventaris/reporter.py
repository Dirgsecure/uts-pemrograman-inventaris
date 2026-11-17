"""Modul pelaporan: format teks dan penyimpanan hasil ke file."""

import csv
import json
from pathlib import Path

from .exceptions import FormatFileError
from .processor import status_stok


def rupiah(angka):
    """Format angka -> 'Rp1.234.000'."""
    return "Rp" + f"{angka:,}".replace(",", ".")


def format_tabel_barang(data, batas=5):
    """Ubah list barang menjadi teks rapi (satu baris per barang)."""
    if not data:
        return "(tidak ada data)"
    baris = [f"{'ID':<7}{'Nama':<24}{'Kategori':<15}{'Jml':>4}  {'Status':<8}"]
    for b in data:
        baris.append(
            f"{b['id_barang']:<7}{b['nama']:<24}{b['kategori']:<15}"
            f"{b['jumlah']:>4}  {status_stok(b['jumlah'], batas):<8}"
        )
    return "\n".join(baris)


def format_rekap(rekap, total_nilai):
    """Ubah dict rekap menjadi teks laporan."""
    if not rekap:
        return "(rekap kosong: tidak ada data)\nTotal nilai aset: " + rupiah(total_nilai)
    baris = []
    for kategori, r in rekap.items():
        baris.append(
            f"- {kategori}: {r['jenis']} jenis, {r['total_unit']} unit, "
            f"nilai {rupiah(r['total_nilai'])}"
        )
    baris.append(f"Total nilai aset: {rupiah(total_nilai)}")
    return "\n".join(baris)


def _siapkan_folder(path):
    path = Path(path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise FormatFileError(f"Tidak bisa membuat folder output: {e}") from e
    return path


def simpan_csv(path, data, kolom):
    """Simpan list of dict ke CSV."""
    path = _siapkan_folder(path)
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            penulis = csv.DictWriter(f, fieldnames=kolom)
            penulis.writeheader()
            penulis.writerows(data)
    except OSError as e:
        raise FormatFileError(f"Gagal menulis {path}: {e}") from e
    return path


def simpan_json(path, obj):
    """Simpan objek Python ke JSON (indent 2, UTF-8)."""
    path = _siapkan_folder(path)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2, ensure_ascii=False)
    except OSError as e:
        raise FormatFileError(f"Gagal menulis {path}: {e}") from e
    return path
