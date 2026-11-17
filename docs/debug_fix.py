"""Versi SETELAH diperbaiki: pakai loader.baca_data() yang memvalidasi tiap baris."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from inventaris import loader, processor

data, galat = loader.baca_data("data/input/inventaris.csv")
unik, _ = processor.hapus_duplikat(data)
print("total nilai:", processor.hitung_total_nilai(unik))
print("baris dilewati:", len(galat))
