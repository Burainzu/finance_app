# 🥤 Aplikasi Pengelola Keuangan - Soda Style

**Aplikasi keuangan pribadi dengan interface yang colorful dan menyegarkan!**

## ✨ Fitur Utama

### 💰 Manajemen Transaksi
- ✅ **Tambah Transaksi** - Catat pemasukan dan pengeluaran dengan detail
- ✅ **Edit Transaksi** - Ubah transaksi yang sudah dibuat (fitur baru!)
- ✅ **Hapus Transaksi** - Menghapus transaksi yang tidak diperlukan
- ✅ **Kategori Transaksi** - Organisir transaksi dengan kategori
- ✅ **Keterangan Detail** - Tambahkan memo untuk setiap transaksi

### 👛 Manajemen Dompet
- ✅ **Buat Dompet** - Buat beberapa dompet untuk berbagai kebutuhan
- ✅ **Lihat Saldo** - Monitor saldo real-time setiap dompet
- ✅ **Hapus Dompet** - Menghapus dompet yang tidak digunakan

### 📊 Analytics & Insights
- ✅ **Total Pemasukan** - Lihat jumlah total uang masuk
- ✅ **Total Pengeluaran** - Lihat jumlah total uang keluar
- ✅ **Saldo Bersih** - Hitung saldo akhir secara otomatis
- ✅ **Filter Transaksi** - Filter berdasarkan tipe (pemasukan/pengeluaran)

### 🎨 Desain (Soda Theme - NEW!)
- ✨ **Warna Cerah & Segar** - Palet warna yang terinspirasi dari minuman soda
- ✨ **Gradient Backgrounds** - Background dengan gradasi warna yang indah
- ✨ **Smooth Animations** - Transisi halus dan responsif
- ✨ **Modern Interface** - Design yang clean dan mudah digunakan

---

## 🚀 Quick Start

### 1. Instalasi Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
streamlit run finance_app.py
```

### 3. Buka di Browser
```
http://localhost:8501
```

---

## 📖 Panduan Penggunaan

### A. Setup Awal
1. **Buat Dompet**
   - Klik bagian "👛 KELOLA DOMPET" di sidebar
   - Pilih "➕ Buat Dompet Baru"
   - Masukkan nama dompet (contoh: Tabungan, Operasional)
   - Klik "✅ Buat Dompet"

2. **Buat Kategori** (Opsional)
   - Klik bagian "📁 KATEGORI" di sidebar  
   - Pilih "➕ Tambah Kategori Baru"
   - Masukkan nama kategori (contoh: Makan, Transport, Hiburan, Gaji)
   - Klik "✅ Tambah Kategori"

### B. Menambah Transaksi
1. Pilih dompet dari dropdown di sidebar
2. Buka tab "📝 Tambah/Edit Transaksi"
3. Isi form:
   - **📅 Tanggal Transaksi** - Kapan transaksi terjadi
   - **💳 Tipe Transaksi** - Pilih "📈 Uang Masuk" atau "📉 Uang Keluar"
   - **💵 Nominal** - Berapa jumlahnya (dalam Rp)
   - **🏷️ Kategori** - Pilih kategori yang sesuai (opsional)
   - **📝 Keterangan** - Tulis penjelasan transaksi
4. Klik "💾 Simpan Transaksi"

### C. Edit Transaksi
1. Buka tab "📋 Daftar Transaksi"
2. Cari transaksi yang ingin diubah
3. Klik tombol "✏️ Edit" di samping transaksi
4. Banner "MODE EDIT" akan muncul di form
5. Ubah data yang ingin diperbarui
6. Klik "💾 Simpan Transaksi" untuk menyimpan perubahan
7. Atau klik "❌ Batal Edit" untuk membatalkan

### D. Lihat Daftar Transaksi
1. Buka tab "📋 Daftar Transaksi"
2. Lihat summary cards (Pemasukan, Pengeluaran, Saldo Bersih)
3. Gunakan filter untuk menyaring:
   - **Semua** - Tampilkan semua transaksi
   - **Pemasukan** - Hanya transaksi uang masuk
   - **Pengeluaran** - Hanya transaksi uang keluar
4. Klik "✏️ Edit" untuk mengubah atau "🗑️" untuk menghapus

---

## 🎨 Soda Theme - Palet Warna

| Warna | Hex Code | Penggunaan |
|-------|----------|-----------|
| 🌸 Pink Cerah | #FF6B9D | Primary, buttons, accents |
| 🌊 Cyan | #00D4FF | Secondary, inputs, highlights |
| 💚 Hijau Neon | #6FFF5E | Success, income indicators |
| ⭐ Kuning | #FFD60A | Warning, wallet balance |
| 🎯 Abu-abu Tua | #1a1a2e | Dark text, borders |

---

## 📁 Struktur File

```
finance_app/
├── finance_app.py           # Main aplikasi Streamlit
├── README.md               # Dokumentasi utama
├── FEATURES_UPDATE.md      # Detail update fitur (v2.0)
├── requirements.txt        # Dependencies
├── finance.db              # Database SQLite (auto-created)
└── README_FINANCE.md       # Dokumentasi lama
```

---

## 💾 Database Schema

### Wallets Table
```sql
CREATE TABLE wallets (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);
```

### Categories Table
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    wallet_id INTEGER,
    date DATE NOT NULL,
    amount REAL NOT NULL,
    type TEXT NOT NULL (CHECK: 'income' or 'expense'),
    description TEXT,
    category_id INTEGER,
    FOREIGN KEY (wallet_id) REFERENCES wallets(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

---

## 🔄 Version History

### v2.0 (Current) - Soda Style Update
- ✨ **NEW:** Enhanced Transaction Edit Feature
- ✨ **NEW:** Colorful Soda Theme dengan warna cerah
- ✨ **NEW:** Improved UI/UX dengan gradient backgrounds
- 🐛 Fixed: Form layout dan styling
- 📈 Enhanced: Validation dan error handling

### v1.0 - Initial Release
- Basic transaction management
- Wallet and category management
- Simple Streamlit interface
- SQLite database

---

## 🛠️ Technical Stack

- **Framework:** Streamlit
- **Database:** SQLite3
- **Data Processing:** Pandas
- **Styling:** Custom CSS dengan Streamlit markdown
- **Language:** Python 3.8+

---

## 📋 Requirements

```
streamlit>=1.28.0
pandas>=2.0.0
```

---

## 💡 Tips & Best Practices

1. **Backup Data**
   - Database disimpan di `finance.db`
   - Backup file ini secara berkala

2. **Gunakan Kategori**
   - Buatlah kategori yang jelas untuk tracking lebih baik
   - Contoh kategori: Gaji, Makan, Transport, Entertainment, Utilities

3. **Catat Detail**
   - Gunakan field keterangan untuk info tambahan
   - Contoh: "Gaji Bulan April", "Makan di Restoran XYZ"

4. **Review Berkala**
   - Periksa transaksi secara berkala
   - Gunakan filter untuk analisis lebih dalam

---

## 🐛 Troubleshooting

### App tidak bisa dijalankan
```bash
# Pastikan semua dependencies terinstall
pip install -r requirements.txt

# Jalankan dengan verbose logging
streamlit run finance_app.py --logger.level=debug
```

### Database corrupted
```bash
# Backup file lama
mv finance.db finance.db.backup

# App akan membuat database baru otomatis
streamlit run finance_app.py
```

### Port 8501 sudah digunakan
```bash
streamlit run finance_app.py --server.port 8502
```

---

## 🤝 Kontribusi

Silakan fork repository ini dan buat pull request untuk:
- Fitur baru
- Bug fixes
- Peningkatan dokumentasi
- Perbaikan UI/UX

---

## 📄 License

Aplikasi ini bebas digunakan untuk keperluan pribadi dan komersial.

---

## 🎉 Nikmati Pengelolaan Keuangan Anda!

Buat rencana keuangan yang lebih baik dengan antarmuka yang menyenangkan dan colorful! 🥤✨

**Untuk detail fitur terbaru, lihat:** [FEATURES_UPDATE.md](FEATURES_UPDATE.md)
