"""Skenario debugging: versi AWAL (buggy) membaca jumlah tanpa validasi."""
import csv

with open("data/input/inventaris.csv", encoding="utf-8") as f:
    total = 0
    for baris in csv.DictReader(f):
        total += int(baris["jumlah"]) * int(baris["harga"])   # BUG: tidak ada validasi
print(total)
