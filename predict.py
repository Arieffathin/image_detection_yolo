from ultralytics import YOLO
import os

# 1. Muat model hasil training deteksi objek
# Pastikan path ke file 'best.pt' Anda sudah benar
model = YOLO(r'runs/detect/train7/weights/best.pt')

# 2. Tentukan path ke satu gambar spesifik yang ingin Anda deteksi
# GANTI baris di bawah ini dengan path lengkap ke file gambar Anda!
# Contoh: path_gambar_spesifik = r'D:\Kuliah\Coding Camp 2025\Model Capstone\Dataset_split_smph\images\train\cardboard\cardboard1.jpg'
# Atau gambar lain yang Anda punya: r'C:\Users\NamaAnda\Pictures\gambar_tes.png'
path_gambar_spesifik = r'Dataset_split_smph\images\train\glass\glass482.jpg'

# 3. (Opsional tapi disarankan) Periksa apakah file gambar benar-benar ada
if not os.path.exists(path_gambar_spesifik):
    raise FileNotFoundError(f"File gambar tidak ditemukan di lokasi: {path_gambar_spesifik}")
else:
    print(f"Gambar yang akan diproses: {path_gambar_spesifik}")

# 4. Lakukan inference pada gambar yang telah ditentukan
# Hasil gambar dengan bounding box akan disimpan.
# Anda bisa mengganti 'project' dan 'name' untuk mengatur folder penyimpanan hasil.
detect_results = model.predict(
    source=path_gambar_spesifik,
    save=True,
    project='runs/detect/inferensi_tunggal',  # Folder utama untuk menyimpan hasil inferensi ini
    name='hasil_deteksi_gambar_spesifik',    # Subfolder spesifik untuk hasil kali ini
    exist_ok=True,                           # Izinkan jika folder sudah ada
    conf=0.25                                # Batas minimum confidence score untuk deteksi
)

# 5. Tampilkan hasil prediksi di terminal
if detect_results: # Memastikan ada hasil deteksi
    for result in detect_results:
        print(f"\n--- Hasil Deteksi untuk: {result.path} ---")
        boxes = result.boxes  # Dapatkan bounding boxes dari hasil
        if len(boxes) == 0:
            print("Tidak ada objek yang terdeteksi pada gambar ini dengan confidence >= 0.25.")
        else:
            for box in boxes:
                cls_id = int(box.cls[0])        # ID kelas objek yang terdeteksi
                confidence = float(box.conf[0]) # Confidence score
                bbox_coords = box.xyxy[0].tolist() # Koordinat bounding box [x1, y1, x2, y2]

                # Untuk mendapatkan nama kelas (misal: "cardboard", "plastic") jika model Anda memilikinya:
                # class_name = model.names[cls_id]
                # print(f"Objek: {class_name} (ID: {cls_id}), Confidence: {confidence:.2f}, Bounding Box: {bbox_coords}")
                print(f"ID Kelas: {cls_id}, Confidence: {confidence:.2f}, Bounding Box: {bbox_coords}")
else:
    print("Proses inferensi tidak menghasilkan output.")

print(f"\nInferensi selesai. Hasil gambar dengan bounding box (jika ada objek terdeteksi) disimpan di folder 'runs/detect/inferensi_tunggal/hasil_deteksi_gambar_spesifik'")