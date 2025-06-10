import io
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)
CORS(app)

# Maksimum file upload: 5MB (opsional)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  

print("🔄 Memuat model YOLO...")
try:
    model = YOLO("best.pt")
    print(f"✅ Model berhasil dimuat. Kelas: {model.names}")
except Exception as e:
    print(f"❌ Gagal memuat model: {e}")
    model = None

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "ok",
        "message": "Server Flask YOLO aktif 🚀",
        "version": "2.0"
    })

@app.route("/predict", methods=["POST"])
def predict():
    print("📩 POST /predict diterima")

    if model is None:
        print("❌ Model tidak tersedia.")
        return jsonify({"status": "error", "message": "Model tidak tersedia."}), 500

    if "image" not in request.files:
        print("⚠️ Tidak ada file gambar dikirim.")
        return jsonify({"status": "error", "message": "Gambar tidak ditemukan dalam request."}), 400

    file = request.files["image"]
    
    # Validasi ekstensi (opsional)
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        return jsonify({"status": "error", "message": "Format file tidak didukung. Gunakan .jpg/.png"}), 400

    try:
        img = Image.open(file.stream).convert("RGB")
        img = img.resize((640, 640))  # resize untuk hemat RAM
        print("📷 Gambar berhasil dibuka dan diresize")

        results = model.predict(img, conf=0.25, verbose=False)
        print("✅ Prediksi selesai")

        detections = []
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            label = model.names.get(cls_id, f"Class_{cls_id}")
            xyxy = [round(float(x), 2) for x in box.xyxy[0]]

            detections.append({
                "jenis_sampah": label,
                "confidence": round(confidence, 2),
                "bounding_box (xyxy)": xyxy
            })

        print(f"🎯 {len(detections)} objek terdeteksi")
        return jsonify({"status": "success", "detections": detections})

    except UnidentifiedImageError:
        print("❌ File bukan gambar valid.")
        return jsonify({"status": "error", "message": "File bukan gambar yang valid."}), 400

    except Exception as e:
        print(f"❌ Error saat prediksi: {e}")
        return jsonify({"status": "error", "message": f"Terjadi kesalahan saat prediksi: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Server berjalan di http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port)
