# Aplikasi Pencatatan Keuangan

Aplikasi pencatatan keuangan sederhana berbasis web menggunakan Streamlit.

## Fitur

- **Multi-Dompet**: Dapat membuat dan mengelola beberapa dompet
- **CRUD Transaksi**: Tambah, edit, dan hapus transaksi keuangan
- **Manajemen Kategori**: Tambah dan kelola kategori transaksi sesuai keinginan
- **Dropdown Kategori**: Kategori dapat digunakan kembali dalam bentuk dropdown
- **Ringkasan Keuangan**: Melihat total pemasukan, pengeluaran, dan saldo

## Data Transaksi

Setiap transaksi mencakup:
- **Tanggal**: Tanggal transaksi
- **Nominal**: Jumlah uang (dalam Rupiah)
- **Tipe**: Uang masuk (income) atau uang keluar (expense)
- **Keterangan**: Deskripsi transaksi
- **Kategori**: Kategori transaksi (dapat ditambahkan sendiri)

## Cara Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Cara Menjalankan

Jalankan aplikasi dengan perintah:
```bash
streamlit run finance_app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

## Cara Penggunaan

1. **Buat Dompet**: Di sidebar, klik "Buat Dompet Baru" dan masukkan nama dompet
2. **Pilih Dompet**: Pilih dompet yang ingin digunakan dari dropdown di sidebar
3. **Tambah Kategori**: Di sidebar, tambahkan kategori yang diinginkan (opsional)
4. **Tambah Transaksi**: 
   - Pilih tab "Tambah/Edit Transaksi"
   - Isi tanggal, nominal, tipe, keterangan, dan kategori
   - Klik "Simpan Transaksi"
5. **Lihat Transaksi**: Pilih tab "Daftar Transaksi" untuk melihat semua transaksi
6. **Edit/Hapus**: Gunakan tombol edit (✏️) atau hapus (🗑️) pada setiap transaksi

## Database

Aplikasi menggunakan SQLite database (`finance.db`) yang akan dibuat otomatis saat pertama kali dijalankan. Data tersimpan secara lokal di direktori yang sama dengan aplikasi.
