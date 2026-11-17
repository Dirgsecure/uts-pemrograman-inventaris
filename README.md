# Aplikasi Inventaris Lab Teknik Komputer (CLI)

UTS Pemrograman Dasar (TK091) - Universitas AMIKOM Yogyakarta, TA 2026/2027
Nama: Dirga Arief Suryadi | Kelas: TK 01 | NIM: (25.83.1182)

## Deskripsi
Aplikasi command line berbasis Python untuk mengolah data inventaris barang laboratorium:
membaca CSV/JSON, memvalidasi, menghapus duplikat, mencari barang, mendeteksi stok
menipis, membuat rekap per kategori, dan menyimpan hasil ke file.

## Persyaratan
- Python 3.8 atau lebih baru
- Hanya standard library (csv, json, argparse, pathlib, unittest). TIDAK ada dependency pihak ketiga,
  jadi tidak perlu `pip install` apa pun.

## Struktur Program
    uts_inventaris/
    |-- main.py                  # titik masuk program
    |-- inventaris/              # package buatan sendiri
    |   |-- __init__.py
    |   |-- exceptions.py        # exception khusus
    |   |-- loader.py            # baca + validasi CSV/JSON
    |   |-- processor.py         # cari, filter, grouping, rekap, hapus duplikat
    |   |-- reporter.py          # format teks + simpan CSV/JSON
    |   `-- cli.py               # argparse + menu interaktif
    |-- data/input/              # contoh input (inventaris.csv, inventaris_kecil.json, dll)
    |-- data/output/             # hasil output
    |-- tests/test_processor.py  # unit test
    `-- docs/                    # skrip demo debugging

Alur dependensi: main.py -> cli -> (loader, processor, reporter). loader dan reporter memakai
exceptions; reporter memakai processor.status_stok. processor tidak bergantung ke modul lain.

## Cara Menjalankan
Buka terminal di folder proyek, lalu:

    python main.py ringkasan
    python main.py cari laptop
    python main.py stok-rendah --batas 5
    python main.py rekap
    python main.py bersihkan
    python main.py menu
    python main.py --input data/input/inventaris_kecil.json rekap



## Format Input
CSV/JSON dengan kolom: id_barang, nama, kategori, jumlah, harga, lokasi, kondisi.
Baris tidak valid (kolom kosong, angka salah, negatif) dilewati dan dilaporkan, bukan membuat program crash.

## Format Output
- Teks di terminal
- data/output/rekap_kategori.json
- data/output/inventaris_bersih.csv dan laporan_kualitas.json

## Menjalankan Unit Test
    python -m unittest discover tests

