---
title: Deteksi Sampah YOLOv8 (Waste Detection)
emoji: 🚮♻️
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.20.0 # Sesuaikan dengan versi Gradio di requirements.txt Anda (misal: 4.29.0)
python_version: 3.9 # Sesuaikan dengan versi Python Anda (misal: 3.10, 3.11)
app_file: app_gradio.py # Sesuaikan jika nama file utama Anda berbeda
pinned: true
license: mit
---

# Deteksi Sampah Menggunakan YOLOv8

Selamat datang di proyek Deteksi Sampah! Proyek ini memanfaatkan model **YOLOv8** untuk mendeteksi dan mengklasifikasikan berbagai jenis sampah ke dalam **6 kelas** berbeda. Aplikasi ini dapat digunakan secara real-time melalui webcam atau dengan mengunggah gambar.

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Notnith/Deteksi-sampah_sprtofy)

**➡️ Kunjungi Aplikasi Web Kami: [Deteksi Sampah Sprtofy di Hugging Face Spaces](https://huggingface.co/spaces/Notnith/Deteksi-sampah_sprtofy) ⬅️**

## 📝 Deskripsi Proyek

Sistem ini dirancang untuk membantu dalam identifikasi dan pemilahan sampah secara otomatis. Dengan memanfaatkan kekuatan model deteksi objek YOLOv8, aplikasi ini mampu mengenali berbagai jenis sampah dengan akurasi tinggi, mendukung upaya pengelolaan sampah yang lebih efisien dan ramah lingkungan.

## ✨ Fitur Utama

* **Deteksi Real-time**: Menggunakan kamera webcam untuk deteksi objek sampah secara langsung.
* **Deteksi via Unggahan Gambar**: Memungkinkan pengguna mengunggah gambar untuk dianalisis.
* **6 Kelas Sampah**: Mampu mendeteksi dan mengklasifikasikan sampah ke dalam kategori berikut:
    1.  Kardus (Cardboard)
    2.  Kaca (Glass)
    3.  Logam (Metal)
    4.  Kertas (Paper)
    5.  Plastik (Plastic)
    6.  Sampah Umum/Lainnya (Trash)
* **Antarmuka Interaktif**: Dibangun menggunakan Gradio untuk kemudahan penggunaan.
* **Akurasi Tinggi**: Model ini mencapai akurasi sebesar **98%** pada dataset pengujian.

## 🚀 Model & Performa

* **Algoritma**: YOLOv8 
* **Akurasi**: 98% (pada dataset validasi/pengujian yang digunakan)
* **Pelatihan**: Model dilatih selama **30 epoch** dengan ukuran **batch (batch size) 8** dan ukuran gambar input **(imgsize) 640x640 piksel**. 

## 💻 Cara Menggunakan Aplikasi Web (Hugging Face Spaces)

1.  Kunjungi tautan: [https://huggingface.co/spaces/Notnith/Deteksi-sampah_sprtofy](https://huggingface.co/spaces/Notnith/Deteksi-sampah_sprtofy)
2.  Anda akan melihat dua tab utama:
    * **"Deteksi via Unggah Gambar"**:
        * Klik atau seret gambar sampah Anda ke kotak unggah.
        * Klik tombol "Submit".
        * Hasil deteksi (gambar dengan bounding box) dan detail JSON (jenis sampah, confidence score, koordinat bounding box) akan ditampilkan.
    * **"Deteksi via Kamera Langsung"**:
        * Izinkan browser untuk mengakses kamera Anda saat diminta.
        * Arahkan kamera ke objek sampah.
        * Hasil deteksi akan ditampilkan secara real-time pada feed kamera beserta detail JSON.
3.  Selesai! Anda bisa membersihkan input dengan tombol "Clear".

![image](https://github.com/user-attachments/assets/abf4d33c-fc0f-4591-9a39-1d45760b2e01)

## 🔧 Setup Lokal (Jika Ingin Menjalankan di Komputer Anda)

Jika Anda ingin menjalankan proyek ini secara lokal untuk pengembangan atau pengujian lebih lanjut:

1.  **Prasyarat**:
    * Python (versi 3.9 atau yang lebih baru direkomendasikan)
    * pip (Python package installer)
    * Git (untuk clone repository)

2.  **Clone Repository**:
    ```bash
    git clone (https://github.com/Arieffathin/image_detection_yolo) # Ganti dengan URL GitHub repo Anda
    cd  image_detection_yolo     # Ganti dengan nama folder repo Anda
    ```

3.  **Buat dan Aktifkan Virtual Environment (Sangat Direkomendasikan)**:
    ```bash
    python -m venv venv
    # Untuk Windows:
    venv\Scripts\activate
    # Untuk macOS/Linux:
    source venv/bin/activate
    ```

4.  **Instal Dependensi**:
    Pastikan Anda memiliki file `requirements.txt` dalam proyek Anda. Kemudian jalankan:
    ```bash
    pip install -r requirements.txt
    ```
    Contoh isi minimal `requirements.txt`:
    ```txt
    torch
    torchvision
    ultralytics
    gradio
    opencv-python
    # Tambahkan library lain jika Anda gunakan
    ```

5.  **Jalankan Aplikasi Gradio**:
    Pastikan file model `best.pt`  berada di direktori yang benar sesuai dengan path yang didefinisikan dalam skrip Python Anda (misalnya, di root folder proyek).
    ```bash
    python app_gradio.py # Atau nama file Python utama Anda
    ```
    Aplikasi akan berjalan dan dapat diakses melalui URL lokal yang ditampilkan di terminal (biasanya `http://127.0.0.1:7860`).

## 🛠️ Teknologi yang Digunakan

* **Python**: Bahasa pemrograman utama.
* **YOLOv8 (Ultralytics)**: Framework untuk model deteksi objek.
* **PyTorch**: Deep learning framework yang menjadi dasar Ultralytics YOLOv8.
* **Gradio**: Untuk membuat antarmuka web interaktif dengan cepat.
* **OpenCV**: Untuk pemrosesan gambar.
* **Hugging Face Spaces**: Platform untuk hosting dan deployment aplikasi ML.

## 💡 Potensi Pengembangan Selanjutnya

* Peningkatan model untuk mengenali lebih banyak sub-kategori sampah.
* Optimasi model (misalnya, kuantisasi) untuk performa yang lebih cepat pada perangkat dengan sumber daya terbatas.
* Integrasi dengan sistem backend untuk pencatatan data sampah dan analisis lebih lanjut.
* Pengembangan fitur untuk estimasi volume atau berat sampah yang terdeteksi.
* Pengembangan aplikasi mobile.

## 🤝 Kontribusi

Kontribusi, isu, dan permintaan fitur sangat diterima! Jangan ragu untuk membuat *pull request* atau membuka *issue* baru.

## 📄 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk detailnya (Anda perlu menambahkan file `LICENSE` jika ingin).

---

Semoga berhasil dengan proyek Anda! Jika ada bagian yang ingin Anda ubah atau tambahkan, beri tahu saya. Anda bisa menyalin dan menempelkan teks di atas ke dalam file `README.md` di repositori GitHub Anda. Jangan lupa untuk mengganti placeholder seperti `[URL_GITHUB_REPOSITORY_ANDA]` dan menyesuaikan versi SDK/Python di YAML frontmatter jika perlu.


