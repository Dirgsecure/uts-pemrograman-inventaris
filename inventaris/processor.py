"""Modul pemroses data: pencarian, filter, grouping, rekap, dedup.

Struktur data yang dipakai:
- list  : menyimpan koleksi barang berurutan (urutan baris file terjaga).
- dict  : 1 barang = 1 dict (kolom -> nilai); juga hasil grouping/rekap.
- set   : cek duplikat id cepat (O(1)) dan daftar kategori unik.
"""


def hapus_duplikat(data):
    """Hapus barang dengan id_barang yang sama (ambil kemunculan pertama).

    Return:
        tuple[list[dict], list[dict]]: (data_unik, data_duplikat).
    """
    id_terlihat = set()
    unik, duplikat = [], []
    for barang in data:
        if barang["id_barang"] in id_terlihat:
            duplikat.append(barang)
        else:
            id_terlihat.add(barang["id_barang"])
            unik.append(barang)
    return unik, duplikat


def cari_barang(data, kata_kunci):
    """Cari barang yang nama/kategori/lokasinya memuat kata_kunci (case-insensitive)."""
    kunci = kata_kunci.strip().lower()
    if not kunci:
        return []
    return [
        b for b in data
        if kunci in b["nama"].lower()
        or kunci in b["kategori"].lower()
        or kunci in b["lokasi"].lower()
    ]


def filter_stok_rendah(data, batas=5):
    """Ambil barang dengan jumlah <= batas, urut dari stok paling sedikit."""
    rendah = [b for b in data if b["jumlah"] <= batas]
    return sorted(rendah, key=lambda b: b["jumlah"])


def daftar_kategori(data):
    """Return set kategori unik (set comprehension)."""
    return {b["kategori"] for b in data}


def kelompokkan_per_kategori(data):
    """Return dict {kategori: [barang, ...]}."""
    kelompok = {k: [] for k in sorted(daftar_kategori(data))}
    for barang in data:
        kelompok[barang["kategori"]].append(barang)
    return kelompok


def rekap_per_kategori(data):
    """Rekap tiap kategori: jenis barang, total unit, total nilai (dict comprehension)."""
    kelompok = kelompokkan_per_kategori(data)
    return {
        kategori: {
            "jenis": len(daftar),
            "total_unit": sum(b["jumlah"] for b in daftar),
            "total_nilai": sum(b["jumlah"] * b["harga"] for b in daftar),
        }
        for kategori, daftar in kelompok.items()
    }


def hitung_total_nilai(data):
    """Total nilai aset = sum(jumlah * harga). Data kosong -> 0 (edge case)."""
    return sum(b["jumlah"] * b["harga"] for b in data)


def status_stok(jumlah, batas=5):
    """Percabangan: kembalikan label status stok."""
    if jumlah == 0:
        return "HABIS"
    elif jumlah <= batas:
        return "MENIPIS"
    return "AMAN"
