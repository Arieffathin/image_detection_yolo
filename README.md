---
title: "Sortify AI – Backend & Machine Learning API"
emoji: "♻️"
colorFrom: "yellow"
colorTo: "green"
sdk: "gradio"
app_file: "app_flask.py"
pinned: false
---

# Sortify AI – Backend & Machine Learning API

<p align="center">
  <img src="Image/huggingface.png" alt="Hugging Face" width="250" style="margin-right: 30px;"/>
  <img src="Image/ultralyticslogo.png" alt="Ultralytics" width="250" style="margin: 0 30px;"/>
  <img src="Image/flasklogo.png" alt="Flask" width="250" style="margin-left: 30px;"/>
</p>

## Overview

... *(lanjutan isi README seperti yang kamu tulis sebelumnya)* ...



---

# Sortify AI – Backend & Machine Learning API

<p align="center">
  <img src="Image/huggingface.png" alt="Hugging Face" width="250" style="margin-right: 30px;"/>
  <img src="Image/ultralyticslogo.png" alt="Ultralytics" width="250" style="margin: 0 30px;"/>
  <img src="Image/flasklogo.png" alt="Flask" width="250" style="margin-left: 30px;"/>
</p>

## Overview

Sortify AI – Backend adalah layanan server untuk platform Sortify AI. Backend ini melayani model deteksi sampah berbasis YOLOv8 melalui REST API, memproses gambar yang diunggah, dan mengembalikan hasil klasifikasi dalam format JSON. Aplikasi ini dikontainerisasi dengan Docker dan dideploy di **Hugging Face Spaces** untuk kemudahan distribusi dan skalabilitas.

---

## Features

* 🤖 **AI-Powered Waste Classification API**
  Endpoint khusus untuk analisis gambar berbasis AI.
* 🧠 **YOLOv8 Model Integration**
  Menggunakan model YOLOv8 terlatih (`best.pt`) untuk mendeteksi 6 jenis sampah.
* 📤 **Image Upload Handling**
  Mendukung pengunggahan gambar via `multipart/form-data`.
* 📦 **Structured JSON Response**
  Hasil deteksi menyertakan jenis sampah, tingkat kepercayaan, dan koordinat bounding box.
* 🐳 **Dockerized for Portability**
  Menjamin konsistensi lingkungan antara development dan production.
* ☁️ **Cloud-Deployed**
  Dihosting secara publik di Hugging Face Spaces untuk integrasi langsung dengan frontend.

---

## Tech Stack

* **Language**: Python 3.9
* **Framework**: Flask
* **Server**: Gunicorn
* **Machine Learning**: YOLOv8 (Ultralytics), PyTorch, OpenCV
* **CORS**: Flask-CORS
* **Containerization**: Docker

---

## Prerequisites

Sebelum menjalankan proyek ini secara lokal, pastikan Anda memiliki:

* Python v3.9 atau lebih tinggi
* pip 
* `virtualenv` 

---

## Getting Started

### 1. Clone repository

```bash
git clone https://github.com/Arieffathin/image_detection_yolo.git
cd image_detection_yolo
```

### 2. Buat dan aktifkan virtual environment

```bash
# Membuat environment
python -m venv venv

# Windows
.\venv\Scripts\activate

# MacOS/Linux
source venv/bin/activate
```

### 3. Instal dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan server lokal

Pastikan file `best.pt` berada di direktori yang sama.

```bash
python app_flask.py
```

Akses server lokal di: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Project Structure

```
.
├── app_flask.py       # Logika utama aplikasi Flask
├── best.pt            # File model YOLOv8 terlatih
├── Dockerfile         # Konfigurasi image Docker
├── requirements.txt   # Daftar dependensi Python
└── README.md          # Dokumentasi proyek
```

---

## Prediction Endpoint

### POST `/predict`

* **URL**:
  `https://notnith-deteksi-sampah-sprtofy.hf.space/predict`
* **Method**: POST
* **Body**: `form-data`

  * **Key**: `image`
  * **Type**: File
  * **Value**: \[Upload file gambar]

####  Response: 200 OK

```json
{
  "status": "success",
  "detections": [
    {
      "waste_type": "cardboard",
      "confidence": 0.85,
      "bounding_box (xyxy)": [101.5, 202.3, 350.1, 450.9]
    }
  ]
}
```

####  Error Response (400/500)

```json
{
  "status": "error",
  "message": "Image file not found in request."
}
```

---

## Deployment

API ini telah dideploy secara publik dan dapat diakses melalui:
**[Hugging Face Spaces](https://huggingface.co/spaces/Notnith/Deteksi-sampah_sprtofy)**



---

## License

Proyek ini dilisensikan di bawah **MIT License**. Lihat file `LICENSE` untuk informasi lebih lanjut.

---

Kontributor [Arief Fathin Abrar] [Gita Karisma] [Harist Islami Ridha]
