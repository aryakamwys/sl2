Ringkasan
Analisis ini mengecek apakah suhu harian di Bandung berbeda pada hari libur vs hari non-libur menggunakan data NASA POWER (temporal/daily/point) untuk tahun 2025 dengan parameter T2M, T2M_MAX, T2M_MIN. Nilai placeholder (mis. −999) dibersihkan, lalu setiap tanggal diberi label libur/non-libur berdasarkan SKB. Ada opsi “jendela libur (±1 hari)” untuk menangkap efek sebelum/sesudah libur. Ringkasan statistik dihitung secara global dan per bulan—mengikuti metode agregasi harian/temporal di dokumentasi POWER.

Alur kerja (singkat)
Ambil data dari NASA POWER untuk koordinat Bandung (−6.9147, 107.6098) → respons JSON deret waktu harian.

Bersihkan data: buang/NaN-kan nilai placeholder (mis. −999).

Label tanggal: tandai libur nasional dari daftar SKB; opsional aktifkan jendela libur ±1 hari.

Pisahkan data: dua kategori — libur dan non-libur.

Agregasi & bandingkan:

Statistik global: mean & median per kategori.

Median per bulan: hanya untuk bulan yang punya data cukup pada keduanya (libur & non-libur).

Visualisasi (opsional): plot ringkasan untuk mempermudah perbandingan.

Keluaran utama
Tabel ringkasan global (mean/median) untuk libur vs non-libur.

Tabel median per bulan untuk kedua kategori (hanya bulan dengan data cukup).

Plot perbandingan (jika diaktifkan).

Kenapa seperti ini?
Konsisten dengan agregasi harian/temporal di dokumentasi NASA POWER.

Jendela libur membantu menangkap efek arus sebelum/sesudah hari H, bukan hanya tepat di tanggal liburnya.

Konfigurasi minimal
Sumber data: NASA POWER Daily API (endpoint temporal/daily/point).

Koordinat: Bandung (−6.9147, 107.6098).

Tahun: 2025.

Parameter: T2M, T2M_MAX, T2M_MIN.

Daftar libur: SKB (format bebas; yang penting bisa dipetakan ke tanggal).

Opsi: aktif/nonaktif jendela libur (±1 hari).

Catatan singkat untuk cuplikan kode
Jika Anda menyertakan screenshot kode di README, tambahkan kalimat ini:
“Bagian A memanggil API dan mem-parse JSON → DataFrame; bagian B membersihkan nilai dan memisahkan baris libur vs non-libur dengan boolean mask; bagian C menghitung ringkasan & membuat plot.”

Replikasi cepat (contoh)
Pastikan dependensi umum: Python 3.10+, pandas, requests, matplotlib (atau library plotting lain).

Sediakan file/daftar SKB.

Jalankan skrip utama untuk: fetch → clean → label → agregasi → (opsional) plot.