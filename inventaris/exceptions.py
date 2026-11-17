"""Exception buatan sendiri agar error mudah dibedakan."""


class InventarisError(Exception):
    """Kelas dasar semua error aplikasi ini."""


class FormatFileError(InventarisError):
    """File tidak ditemukan, kosong, atau formatnya tidak didukung."""


class DataTidakValidError(InventarisError):
    """Sebuah baris data melanggar aturan validasi."""
