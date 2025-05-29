import cv2
from ultralytics import YOLO

# 1. Tentukan Path ke Model YOLO Anda
MODEL_PATH = r'runs/detect/train7/weights/best.pt' # Sesuaikan jika perlu

print("Mencoba memuat model YOLO...")
try:
    model = YOLO(MODEL_PATH)
    print(f"Model YOLO berhasil dimuat dari: {MODEL_PATH}")
except Exception as e:
    print(f"Error saat memuat model YOLO: {e}")
    exit() # Keluar jika model gagal dimuat

# 2. Inisialisasi Kamera <-- PERHATIKAN BAGIAN INI
CAMERA_INDEX = 0  # Biasanya 0 untuk webcam internal
cap = cv2.VideoCapture(CAMERA_INDEX)  # <--- 'cap' DIDEFINISIKAN DI SINI

# Periksa apakah kamera berhasil dibuka
if not cap.isOpened():
    print(f"Error: Tidak dapat membuka kamera dengan index {CAMERA_INDEX}.")
    print("Pastikan kamera terhubung dan tidak digunakan aplikasi lain.")
    exit() # Keluar jika kamera gagal dibuka
# else: # Tidak perlu else jika sudah exit di atas
print(f"Kamera dengan index {CAMERA_INDEX} berhasil dibuka.")
print("Tekan tombol 'q' pada jendela kamera untuk keluar.")


# Dapatkan nama-nama kelas dari model (jika tersedia)
class_names = model.names
if class_names:
    print(f"Nama kelas yang dikenali oleh model: {class_names}")
else:
    print("Tidak dapat mengambil nama kelas dari model. Akan ditampilkan sebagai Class ID.")


# Debugging tambahan yang saya sarankan sebelumnya
print("\n--- MEMULAI LOOP KAMERA ---")
loop_counter = 0

# Loop utama untuk memproses frame kamera
while True:
    loop_counter += 1
    print(f"\n>>> Iterasi Loop Ke-{loop_counter} Dimulai <<<")

    success, frame = cap.read()  # <--- 'cap' DIGUNAKAN DI SINI
    if not success:
        print(f"Iterasi {loop_counter}: GAGAL membaca frame dari kamera.")
        break
    
    # (lanjutan kode di dalam loop... seperti model.predict(), dll.)
    # ...
    # Pastikan Anda menyalin semua bagian dalam loop yang sudah saya berikan sebelumnya
    # ...
    print(f"Iterasi {loop_counter}: Akan memanggil model.predict()...")
    try:
        results = model.predict(source=frame, conf=0.15, verbose=False)
        print(f"Iterasi {loop_counter}: model.predict() SELESAI dipanggil.")

        if results and len(results) > 0:
            result_frame = results[0]
            boxes = result_frame.boxes
            print(f"Iterasi {loop_counter}: Jumlah box terdeteksi: {len(boxes)}")

            # (sisanya untuk menggambar box dan menampilkan info deteksi)
            # ... (Salin dari snippet saya sebelumnya) ...
            if len(boxes) > 0:
                print(f"   Detail deteksi di iterasi {loop_counter}:")
                for i, box_item in enumerate(boxes): # Ganti 'box' menjadi 'box_item' agar tidak konflik dengan variabel di luar
                    cls_id = int(box_item.cls[0])
                    confidence_score = float(box_item.conf[0])
                    class_name_debug = class_names.get(cls_id, f"ID:{cls_id}") if class_names else f"ID:{cls_id}"
                    coords_debug = [int(c) for c in box_item.xyxy[0]]
                    print(f"     - Box {i+1}: Kelas='{class_name_debug}', Confidence={confidence_score:.2f}, Koordinat={coords_debug}")

            for box_item in boxes: # Ganti 'box' menjadi 'box_item'
                x1, y1, x2, y2 = map(int, box_item.xyxy[0])
                confidence = float(box_item.conf[0])
                cls_id = int(box_item.cls[0])
                class_name = class_names.get(cls_id, f"ID:{cls_id}") if class_names else f"ID:{cls_id}"
                label = f"{class_name} {confidence:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        else:
            print(f"Iterasi {loop_counter}: Model tidak mengembalikan 'results' atau 'results' kosong.")
    
    except Exception as e:
        print(f"Iterasi {loop_counter}: TERJADI ERROR saat prediksi atau pemrosesan hasil: {e}")
        break 

    cv2.imshow("Deteksi Objek Kamera Langsung (Tekan 'q' untuk keluar)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Tombol 'q' ditekan. Menutup program...")
        break

# Setelah loop selesai
print("\n--- LOOP KAMERA SELESAI ---")

# Melepaskan kamera dan menutup jendela
# Cek dulu apakah 'cap' terdefinisi dan kameranya terbuka sebelum mencoba melepaskannya
if 'cap' in locals() and cap.isOpened():
    print("Melepaskan sumber daya kamera...")
    cap.release()
else:
    # Ini bisa terjadi jika loop tidak pernah dimulai karena kamera gagal dibuka
    print("Variabel 'cap' tidak terdefinisi dengan benar atau kamera tidak dibuka, tidak perlu dilepaskan.")

cv2.destroyAllWindows()
print("Semua jendela OpenCV telah ditutup.")