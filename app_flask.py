import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)
CORS(app)

# Load model sekali saat start
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
        "version": "3.0"
    })

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"status": "error", "message": "Model tidak tersedia"}), 500

    if "image" not in request.files:
        return jsonify({"status": "error", "message": "Gambar tidak ditemukan"}), 400

    try:
        file = request.files["image"]
        img = Image.open(file.stream).convert("RGB")
        img = img.resize((640, 640))  # Supaya ringan

        results = model.predict(img, conf=0.25, verbose=False)

        detections = []
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            label = model.names.get(cls_id, f"Class_{cls_id}")
            confidence = float(box.conf[0])
            bbox = [round(float(x), 2) for x in box.xyxy[0]]

            detections.append({
                "jenis_sampah": label,
                "confidence": round(confidence, 2),
                "bounding_box (xyxy)": bbox
            })

        return jsonify({"status": "success", "detections": detections})

    except UnidentifiedImageError:
        return jsonify({"status": "error", "message": "File bukan gambar valid"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"Gagal memproses gambar: {e}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
