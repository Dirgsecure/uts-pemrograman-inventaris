"""Unit test (unittest, standard library). Jalankan: python -m unittest discover tests"""
import unittest

from inventaris import loader, processor
from inventaris.exceptions import DataTidakValidError


def barang(id_, jumlah, harga=1000, kategori="A"):
    return {"id_barang": id_, "nama": f"Brg {id_}", "kategori": kategori,
            "jumlah": jumlah, "harga": harga, "lokasi": "L1", "kondisi": "Baik"}


class TestProcessor(unittest.TestCase):
    def test_hapus_duplikat(self):
        unik, dup = processor.hapus_duplikat([barang("1", 1), barang("1", 1), barang("2", 1)])
        self.assertEqual(len(unik), 2)
        self.assertEqual(len(dup), 1)

    def test_total_nilai_data_kosong(self):          # edge case
        self.assertEqual(processor.hitung_total_nilai([]), 0)

    def test_rekap_data_kosong(self):                # edge case
        self.assertEqual(processor.rekap_per_kategori([]), {})

    def test_status_stok(self):
        self.assertEqual(processor.status_stok(0), "HABIS")
        self.assertEqual(processor.status_stok(3), "MENIPIS")
        self.assertEqual(processor.status_stok(50), "AMAN")

    def test_validasi_angka_salah(self):
        mentah = barang("1", "abc")
        with self.assertRaises(DataTidakValidError):
            loader.validasi_baris(mentah, 2)


if __name__ == "__main__":
    unittest.main()
