# Analisis Pengaruh Hari Libur terhadap Suhu Harian Bandung (NASA POWER, 2025)

> TL;DR — Membandingkan suhu harian **libur vs non-libur** di Bandung (2025) dari **NASA POWER**. Nilai placeholder dibersihkan, tanggal dilabeli berdasarkan **SKB**, tersedia opsi **jendela libur ±1 hari**, lalu dihitung ringkasan **global** dan **per bulan**.

---

## Tabel Isi
- [Ringkasan](#ringkasan)
- [Dataset & Konfigurasi](#dataset--konfigurasi)
- [Alur Kerja](#alur-kerja)
- [Keluaran](#keluaran)
- [Cara Pakai (Quickstart)](#cara-pakai-quickstart)
- [Catatan untuk Screenshot Kode](#catatan-untuk-screenshot-kode)
- [Struktur Proyek (opsional)](#struktur-proyek-opsional)
- [Referensi (APA 7th)](#referensi-apa-7th)
- [Lisensi](#lisensi)

---

## Ringkasan
Analisis ini mengecek apakah suhu harian di Bandung berbeda pada **hari libur** vs **hari non-libur** menggunakan data **NASA POWER** (endpoint `temporal/daily/point`) untuk tahun **2025** dengan parameter **T2M, T2M_MAX, T2M_MIN**. Nilai placeholder (mis. **−999**) dibersihkan, lalu setiap tanggal diberi label libur/non-libur berdasarkan **SKB**. Ada opsi **“jendela libur (±1 hari)”** untuk menangkap efek sebelum/sesudah libur. Ringkasan statistik dihitung secara **global** dan **per bulan**, konsisten dengan metode agregasi harian/temporal di dokumentasi POWER.

---

## Dataset & Konfigurasi
- **Sumber data**: NASA POWER Daily API (`temporal/daily/point`)
- **Koordinat**: Bandung **(−6.9147, 107.6098)**
- **Tahun**: **2025**
- **Parameter**: `T2M`, `T2M_MAX`, `T2M_MIN`
- **Placeholder**: nilai seperti **−999** dibuang/di-NaN-kan
- **Daftar libur**: **SKB** (format apa pun, asalkan bisa dipetakan ke tanggal)
- **Opsi**: **jendela libur (±1 hari)** untuk menangkap efek sebelum/sesudah hari H

---

## Alur Kerja
1. **Ambil data** dari NASA POWER → respons JSON deret waktu harian untuk koordinat Bandung.  
2. **Bersihkan data**: buang/NaN-kan nilai placeholder (mis. −999).  
3. **Label tanggal**: tandai libur nasional dari daftar SKB; opsional aktifkan **jendela libur ±1 hari**.  
4. **Pisahkan data** menjadi **libur** dan **non-libur**.  
5. **Agregasi & bandingkan**:
   - **Statistik global**: mean & median per kategori.
   - **Median per bulan**: hanya untuk bulan yang punya data **cukup** pada **keduanya** (libur & non-libur).
6. **Visualisasi (opsional)**: plot ringkasan untuk mempermudah perbandingan.

---

## Keluaran
- **Tabel ringkasan global** (mean/median) untuk libur vs non-libur  
- **Tabel median per bulan** (hanya bulan dengan data cukup pada kedua kategori)  
- **Plot** perbandingan (opsional)

---

## Cara Pakai (Quickstart)

### 1) Persiapan
```bash
# (opsional) buat dan aktifkan virtualenv
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python main.py

# install dependensi minimum
pip install pandas requests matplotlib python-dateutil
