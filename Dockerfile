# ====================================================================
# DOCKERFILE FINAL - MENGGUNAKAN TEKNIK MULTI-STAGE UNTUK MENGECILKAN UKURAN
# ====================================================================

# --- PANGGUNG 1: "BUILDER" ---
# Kita gunakan image penuh untuk build agar semua alat tersedia
FROM python:3.9 as builder

# Install dependensi sistem di sini
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN python -m venv /opt/venv


ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

COPY . .


ENV PATH="/opt/venv/bin:$PATH"

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:7860", "app_flask:app"]
