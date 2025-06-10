import io
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'best.pt'

print("🔄 Memuat model YOLO...")
try:
    model_yolo = YOLO(MODEL_PATH)
    print(f"✅ Model berhasil dimuat. Kelas: {model_yolo.names}")
except Exception as e:
    print(f"❌ Gagal memuat model YOLO: {e}")
    model_yolo = None

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "Selamat! Server Flask v2 sedang berjalan!",
        "version": "2.0"
    })

@app.route('/predict', methods=['POST'])
def predict():
    print("📩 Menerima request ke /predict")

    if model_yolo is None:
        return jsonify({'status': 'error', 'message': 'Model tidak tersedia atau gagal dimuat.'}), 500

    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'File gambar tidak ditemukan dalam request.'}), 400

    file = request.files['image']

    try:
        img = Image.open(file.stream).convert("RGB")
        img = img.resize((640, 640))  # ✅ Resize DI SINI, bukan di luar route

        results = model_yolo.predict(source=img, conf=0.25, verbose=False)

        detected_objects_list = []
        if results and results[0].boxes.shape[0] > 0:
            print(f"✅ Objek terdeteksi: {len(results[0].boxes)}")
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model_yolo.names.get(cls_id, f"ID_Kelas:{cls_id}")

                detected_objects_list.append({
                    "jenis_sampah": class_name,
                    "confidence": round(confidence, 2),
                    "bounding_box (xyxy)": [round(coord, 2) for coord in box.xyxy[0].tolist()]
                })
        else:
            print("🔍 Tidak ada objek yang terdeteksi.")

        return jsonify({
            'status': 'success',
            'detections': detected_objects_list
        })

    except UnidentifiedImageError:
        print("❌ File bukan gambar valid.")
        return jsonify({'status': 'error', 'message': 'File bukan gambar yang valid.'}), 400

    except Exception as e:
        print(f"❌ Error saat prediksi: {e}")
        return jsonify({'status': 'error', 'message': f'Terjadi kesalahan saat pemrosesan: {e}'}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Server dijalankan di port {port}")
    app.run(host="0.0.0.0", port=port)
