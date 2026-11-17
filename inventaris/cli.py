"""Modul antarmuka command line (argparse + menu interaktif)."""

import argparse
import sys

from . import loader, processor, reporter
from .exceptions import InventarisError

KOLOM = loader.KOLOM_WAJIB


def muat_dan_bersihkan(path):
    """Baca file lalu hapus duplikat.

    Return:
        tuple[list[dict], list[str], list[dict]]: (data_unik, galat, duplikat).
    """
    valid, galat = loader.baca_data(path)
    unik, duplikat = processor.hapus_duplikat(valid)
    return unik, galat, duplikat


def minta_angka(pesan, default):
    """Minta input angka bulat >= 0; ulangi sampai valid (defensive input)."""
    while True:
        teks = input(f"{pesan} [default {default}]: ").strip()
        if teks == "":
            return default
        try:
            nilai = int(teks)
        except ValueError:
            print("  ! Masukkan angka bulat, contoh: 5")
            continue
        if nilai < 0:
            print("  ! Angka tidak boleh negatif")
            continue
        return nilai


def jalankan_menu(data):
    """Menu interaktif sampai pengguna memilih keluar."""
    while True:
        print("\n=== MENU INVENTARIS LAB ===")
        print("1. Lihat semua barang\n2. Cari barang\n3. Stok rendah")
        print("4. Rekap per kategori\n0. Keluar")
        try:
            pilihan = input("Pilih menu: ").strip()
        except EOFError:
            print("\nInput berakhir, keluar.")
            return
        if pilihan == "1":
            print(reporter.format_tabel_barang(data))
        elif pilihan == "2":
            kunci = input("Kata kunci: ")
            print(reporter.format_tabel_barang(processor.cari_barang(data, kunci)))
        elif pilihan == "3":
            batas = minta_angka("Batas stok", 5)
            print(reporter.format_tabel_barang(processor.filter_stok_rendah(data, batas), batas))
        elif pilihan == "4":
            print(reporter.format_rekap(
                processor.rekap_per_kategori(data), processor.hitung_total_nilai(data)))
        elif pilihan == "0":
            print("Sampai jumpa.")
            return
        else:
            print("  ! Pilihan tidak dikenal, coba lagi.")


def buat_parser():
    p = argparse.ArgumentParser(prog="main.py", description="Aplikasi inventaris Lab TK")
    p.add_argument("--input", default="data/input/inventaris.csv", help="file .csv/.json")
    p.add_argument("--output-dir", default="data/output", help="folder hasil")
    sub = p.add_subparsers(dest="perintah", required=True)
    sub.add_parser("ringkasan", help="ringkasan data + laporan kualitas data")
    c = sub.add_parser("cari", help="cari barang")
    c.add_argument("kata_kunci")
    s = sub.add_parser("stok-rendah", help="barang dengan stok menipis")
    s.add_argument("--batas", type=int, default=5)
    sub.add_parser("rekap", help="rekap per kategori + simpan ke file")
    sub.add_parser("bersihkan", help="simpan data bersih (tanpa duplikat/error)")
    sub.add_parser("menu", help="menu interaktif")
    return p


def main(argv=None):
    """Titik masuk program. Return 0 jika sukses, 1 jika error terduga."""
    args = buat_parser().parse_args(argv)
    try:
        data, galat, duplikat = muat_dan_bersihkan(args.input)
    except InventarisError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return 1

    if args.perintah == "ringkasan":
        print(f"Barang valid & unik : {len(data)}")
        print(f"Duplikat dibuang    : {len(duplikat)} -> {[d['id_barang'] for d in duplikat]}")
        print(f"Baris error         : {len(galat)}")
        for pesan in galat:
            print(f"  ! {pesan}")
        print(f"Kategori            : {sorted(processor.daftar_kategori(data))}")
    elif args.perintah == "cari":
        print(reporter.format_tabel_barang(processor.cari_barang(data, args.kata_kunci)))
    elif args.perintah == "stok-rendah":
        if args.batas < 0:
            print("[ERROR] --batas tidak boleh negatif", file=sys.stderr)
            return 1
        print(reporter.format_tabel_barang(
            processor.filter_stok_rendah(data, args.batas), args.batas))
    elif args.perintah == "rekap":
        rekap = processor.rekap_per_kategori(data)
        total = processor.hitung_total_nilai(data)
        print(reporter.format_rekap(rekap, total))
        try:
            reporter.simpan_json(f"{args.output_dir}/rekap_kategori.json",
                                 {"rekap": rekap, "total_nilai": total})
            print(f"Tersimpan: {args.output_dir}/rekap_kategori.json")
        except InventarisError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1
    elif args.perintah == "bersihkan":
        try:
            reporter.simpan_csv(f"{args.output_dir}/inventaris_bersih.csv", data, KOLOM)
            reporter.simpan_json(f"{args.output_dir}/laporan_kualitas.json",
                                 {"valid_unik": len(data), "duplikat": len(duplikat),
                                  "error": galat})
            print(f"Tersimpan {len(data)} baris bersih ke {args.output_dir}/inventaris_bersih.csv")
        except InventarisError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1
    elif args.perintah == "menu":
        jalankan_menu(data)
    return 0
