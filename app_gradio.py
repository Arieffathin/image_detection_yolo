

import gradio as gr
from ultralytics import YOLO
import torch


MODEL_PATH = 'D:/Kuliah/Coding Camp 2025/Model Capstone/runs/detect/train7/weights/best.pt'

print("Mencoba memuat model YOLO...")
try:
    model_yolo = YOLO(MODEL_PATH)

    print(f"Model YOLO berhasil dimuat dari: {MODEL_PATH}")
    print(f"Nama kelas yang dikenali model: {model_yolo.names}") 
except Exception as e:
    print(f"Error saat memuat model YOLO: {e}")
    model_yolo = None


def deteksi_gambar_unggahan(gambar_input_dari_pengguna):
    if model_yolo is None:
        return None, {"error": "Model gagal dimuat."}
    if gambar_input_dari_pengguna is None:
        return None, {"error": "Tidak ada gambar yang diunggah."}

    print("Menerima gambar unggahan, melakukan prediksi...")
    try:
        results = model_yolo.predict(source=gambar_input_dari_pengguna, conf=0.25, verbose=False)
        
        detected_objects_list = []
        gambar_hasil_plot = gambar_input_dari_pengguna 

        if results and results[0].boxes.shape[0] > 0:
            gambar_hasil_plot = results[0].plot() 

            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])
       
                class_name = model_yolo.names.get(cls_id, f"ID_Kelas:{cls_id}")
                
                detected_objects_list.append({
                    "jenis_sampah": class_name,
                    "confidence": round(confidence, 2),
                    "bounding_box (xyxy)": [round(coord, 2) for coord in box.xyxy[0].tolist()]
                })
            print(f"Objek terdeteksi: {detected_objects_list}")
        else:
            print("Tidak ada objek yang terdeteksi pada gambar unggahan.")

        return gambar_hasil_plot, detected_objects_list

    except Exception as e:
        print(f"Error saat prediksi pada gambar unggahan: {e}")
        return None, {"error": str(e)}


def deteksi_kamera_langsung(frame_dari_kamera_pengguna):
    if model_yolo is None:
        return None, {"error": "Model gagal dimuat."} 
    if frame_dari_kamera_pengguna is None:
        return None, {"error": "Tidak ada frame dari kamera."} 
    print("Menerima frame dari kamera pengguna, melakukan prediksi...")
    try:
        results = model_yolo.predict(source=frame_dari_kamera_pengguna, conf=0.15, verbose=False)
        
        detected_objects_list = []
        gambar_hasil_plot = frame_dari_kamera_pengguna # Default ke frame asli jika tidak ada deteksi

        if results and results[0].boxes.shape[0] > 0:
            gambar_hasil_plot = results[0].plot()

            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model_yolo.names.get(cls_id, f"ID_Kelas:{cls_id}")
                
                detected_objects_list.append({
                    "jenis_sampah": class_name,
                    "confidence": round(confidence, 2)
                })


        return gambar_hasil_plot, detected_objects_list

    except Exception as e:
        
        print(f"Error saat prediksi pada frame kamera: {e}")
        return frame_dari_kamera_pengguna, {"error": str(e)}



antarmuka_unggah = gr.Interface(
    fn=deteksi_gambar_unggahan,
    inputs=gr.Image(type="pil", label="Unggah Gambar Anda"),
    outputs=[
        gr.Image(type="numpy", label="Gambar Hasil Deteksi"),
        gr.JSON(label="Detail Deteksi JSON") # Output JSON akan menampilkan list objek terdeteksi
    ],
    title="Deteksi Objek dari Gambar Unggahan",
    description="Unggah gambar untuk dideteksi objeknya. Model dapat mengenali: cardboard, metal, glass, paper, trash, plastic."
)

antarmuka_kamera = gr.Interface(
    fn=deteksi_kamera_langsung,
    inputs=gr.Image(sources="webcam", type="numpy", streaming=True, label="Kamera Anda"),
    outputs=[
        gr.Image(type="numpy", label="Kamera dengan Deteksi"),
        gr.JSON(label="Detail Deteksi JSON") #a
    ],
    live=True,
    title="Deteksi Objek dari Kamera Langsung",
    description="Izinkan akses kamera. Model dapat mengenali: cardboard, metal, glass, paper, trash, plastic."
)

aplikasi_tab = gr.TabbedInterface(
    [antarmuka_unggah, antarmuka_kamera],
    ["Deteksi via Unggah Gambar", "Deteksi via Kamera Langsung"]
)

if __name__ == "__main__":
    if model_yolo is None:
        print("PERINGATAN: Model YOLO tidak berhasil dimuat. Aplikasi Gradio mungkin tidak berfungsi dengan benar.")
    else:
        # Verifikasi nama kelas setelah model dimuat
        # Pastikan urutan dan nama kelas ini sesuai dengan training model Anda
        # Contoh: {0: 'cardboard', 1: 'glass', 2: 'metal', 3: 'paper', 4: 'plastic', 5: 'trash'}
        print("Nama kelas yang terdaftar di model:")
        for class_id, class_name in model_yolo.names.items():
            print(f"  ID: {class_id}, Nama: {class_name}")

    aplikasi_tab.launch()