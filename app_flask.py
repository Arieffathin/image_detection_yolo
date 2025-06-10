import io
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)
CORS(app)

print("🔄 Memuat model YOLO...")
try:
    model = YOLO("best.pt")
    print(f"✅ Model berhasil dimuat dengan kelas: {model.names}")
except Exception as e:
    print(f"❌ Gagal memuat model: {e}")
    model = None

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "ok",
        "message": "Server Flask v2 aktif 🚀",
        "version": "2.0"
    })

@app.route("/predict", methods=["POST"])
def predict():
    print("📩 Menerima POST /predict")

    if model is None:
        print("❌ Model belum tersedia.")
        return jsonify({"status": "error", "message": "Model tidak tersedia."}), 500

    if 'image' not in request.files:
        print("⚠️ Gambar tidak dikirim.")
        return jsonify({"status": "error", "message": "Gambar tidak ditemukan dalam request."}), 400

    try:
        file = request.files['image']
        img = Image.open(file.stream).convert("RGB")

        # Resize gambar agar tidak boros memori
        img = img.resize((640, 640))

        print("🧠 Melakukan prediksi...")
        results = model.predict(img, conf=0.25, verbose=False)

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

        print(f"✅ Ditemukan {len(detections)} objek")
        return jsonify({"status": "success", "detections": detections})

    except UnidentifiedImageError:
        print("❌ Gagal membuka gambar.")
        return jsonify({"status": "error", "message": "File bukan gambar valid."}), 400

    except Exception as e:
        print(f"❌ Error saat prediksi: {e}")
        return jsonify({"status": "error", "message": f"Terjadi kesalahan: {e}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
