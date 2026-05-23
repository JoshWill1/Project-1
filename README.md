# Portofolio Cerdas & AI Spam Filter

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Framework-black.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange.svg)](https://scikit-learn.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)](https://www.sqlite.org/)

Sebuah aplikasi Full-Stack Web berbasis Python dengan sistem manajemen portofolio interaktif dengan model Natural Language Processing (NLP). Sistem ini menggunakan Machine Learning untuk menganalisis dan memisahkan pesan kontak organik dari pesan spam secara otomatis.

🌐 Lihat & coba di Sini -> [https://joshua0112.pythonanywhere.com/]

---

# Fitur Utama

1. Dashboard Admin Tersentralisasi: Sistem autentikasi (Login/Register) dengan manajemen sesi Flask yang aman untuk mengakses dasbor kontrol.
2. Manajemen Portofolio (CRUD): Admin dapat menambahkan, melihat, dan menghapus daftar proyek pengalaman kerja secara real-time ke dalam database.
3. AI Spam Detector: Menggunakan algoritma Naive Bayes untuk memindai pesan masuk dari pengunjung dan melabelinya sebagai `[PENTING]`, `[SPAM]`, atau `[BIASA]`.
4. Antarmuka Responsif: Desain UI/UX menggunakan HTML5 dan CSS3 murni dengan mobile-first dan gradient background modern.

---

# Arsitektur Sistem

Aplikasi ini dibangun menggunakan arsitektur pemisahan tugas (MVC pattern):
* Frontend: Menangani interaksi pengguna (Forms, Buttons, Layout) menggunakan Jinja2 Templating Engine.
* Backend: Flask bertindak sebagai controller yang mengatur logika rute (URL) dan autentikasi.
* Database: SQLite3 bertindak sebagai media penyimpanan persisten yang terbagi dalam dua laci utama (`users` dan `messages/projects`).
* AI Model: Teks masukan diekstraksi menggunakan `CountVectorizer` dan diprediksi menggunakan model klasifikasi `MultinomialNB` dari Scikit-Learn yang dimuat melalui modul `pickle`.

# Tentang Pengembang
Joshua William
Mahasiswa IT semester 6 di Binus Online dengan fokus utama pada infrastruktur teknologi, Jaringan, Basis Data Relasional, dan Kecerdasan Buatan (AI/ML).

Email: (williamjoshua011203@gmail.com)