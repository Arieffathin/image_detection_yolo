import os
import shutil
import random

# --- KONFIGURASI ---
# Ganti path berikut sesuai dengan kebutuhan Anda
SOURCE_DIR = r'D:\Kuliah\Coding Camp 2025\Model Capstone\trashnet\dataset-original'  # Contoh: r'D:\Dataset\hewan'
DEST_DIR = r'D:\Kuliah\Coding Camp 2025\Model Capstone\Dataset_split_smph' # Contoh: r'D:\Dataset\hewan_split'
TRAIN_RATIO = 0.8  # 80% untuk data training, 20% untuk data validasi
RANDOM_SEED = 42   # Seed untuk random shuffle agar hasil split konsisten

# Ekstensi file gambar yang didukung
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
# -------------------

def create_dir_if_not_exists(path):
    """Membuat direktori jika belum ada."""
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f"Direktori '{path}' sudah ada.")

def split_data_and_labels():
    """
    Fungsi utama untuk membagi dataset gambar dan membuat file label.
    """
    print(f"Memulai proses split dataset...")
    print(f"Direktori Sumber: {SOURCE_DIR}")
    print(f"Direktori Tujuan: {DEST_DIR}")
    print(f"Rasio Training: {TRAIN_RATIO*100}%")

    if not os.path.isdir(SOURCE_DIR):
        print(f"Error: Direktori sumber '{SOURCE_DIR}' tidak ditemukan atau bukan direktori.")
        return

    # Atur seed untuk reproduktifitas
    random.seed(RANDOM_SEED)

    # Hapus direktori tujuan jika sudah ada untuk memulai dari bersih (opsional)
    if os.path.exists(DEST_DIR):
        print(f"Menghapus direktori tujuan yang sudah ada: '{DEST_DIR}'")
        shutil.rmtree(DEST_DIR)
    
    # Path untuk output
    output_img_train_dir = os.path.join(DEST_DIR, 'images', 'train')
    output_img_val_dir = os.path.join(DEST_DIR, 'images', 'val')
    output_lbl_train_dir = os.path.join(DEST_DIR, 'labels', 'train')
    output_lbl_val_dir = os.path.join(DEST_DIR, 'labels', 'val')

    # Membuat direktori dasar
    create_dir_if_not_exists(output_img_train_dir)
    create_dir_if_not_exists(output_img_val_dir)
    create_dir_if_not_exists(output_lbl_train_dir)
    create_dir_if_not_exists(output_lbl_val_dir)

    class_names = [d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))]
    
    if not class_names:
        print(f"Tidak ada subdirektori kelas yang ditemukan di '{SOURCE_DIR}'. Pastikan dataset Anda terstruktur dengan subdirektori per kelas.")
        return

    print(f"Ditemukan {len(class_names)} kelas: {', '.join(class_names)}")

    for class_index, class_name in enumerate(class_names):
        print(f"\nMemproses kelas: {class_name} (Indeks: {class_index})")
        
        source_class_dir = os.path.join(SOURCE_DIR, class_name)
        
        # Membuat subdirektori kelas di dalam folder train/val untuk images dan labels
        dest_img_train_class_dir = os.path.join(output_img_train_dir, class_name)
        dest_img_val_class_dir = os.path.join(output_img_val_dir, class_name)
        dest_lbl_train_class_dir = os.path.join(output_lbl_train_dir, class_name)
        dest_lbl_val_class_dir = os.path.join(output_lbl_val_dir, class_name)

        create_dir_if_not_exists(dest_img_train_class_dir)
        create_dir_if_not_exists(dest_img_val_class_dir)
        create_dir_if_not_exists(dest_lbl_train_class_dir)
        create_dir_if_not_exists(dest_lbl_val_class_dir)

        image_files = [
            f for f in os.listdir(source_class_dir) 
            if os.path.isfile(os.path.join(source_class_dir, f)) and f.lower().endswith(SUPPORTED_EXTENSIONS)
        ]
        
        if not image_files:
            print(f"  Tidak ada file gambar yang ditemukan di '{source_class_dir}' untuk kelas '{class_name}'.")
            continue

        random.shuffle(image_files) # Acak urutan file
        
        split_point = int(len(image_files) * TRAIN_RATIO)
        train_files = image_files[:split_point]
        val_files = image_files[split_point:]

        print(f"  Total gambar: {len(image_files)}")
        print(f"  Jumlah data training: {len(train_files)}")
        print(f"  Jumlah data validasi: {len(val_files)}")

        # Proses file training
        for image_filename in train_files:
            # Salin file gambar
            source_image_path = os.path.join(source_class_dir, image_filename)
            dest_image_path = os.path.join(dest_img_train_class_dir, image_filename)
            shutil.copy2(source_image_path, dest_image_path)
            
            # Buat file label
            label_filename = os.path.splitext(image_filename)[0] + '.txt'
            dest_label_path = os.path.join(dest_lbl_train_class_dir, label_filename)
            with open(dest_label_path, 'w') as f_label:
                # Format: class_index center_x center_y width height (normalized)
                # Ini adalah label default yang mencakup seluruh gambar.
                f_label.write(f"{class_index} 0.5 0.5 1.0 1.0\n")
        
        # Proses file validasi
        for image_filename in val_files:
            # Salin file gambar
            source_image_path = os.path.join(source_class_dir, image_filename)
            dest_image_path = os.path.join(dest_img_val_class_dir, image_filename)
            shutil.copy2(source_image_path, dest_image_path)
            
            # Buat file label
            label_filename = os.path.splitext(image_filename)[0] + '.txt'
            dest_label_path = os.path.join(dest_lbl_val_class_dir, label_filename)
            with open(dest_label_path, 'w') as f_label:
                f_label.write(f"{class_index} 0.5 0.5 1.0 1.0\n")
                
    print("\nProses split dataset dan pembuatan label selesai.")
    print(f"Dataset yang telah diproses tersedia di: '{DEST_DIR}'")
    print("Struktur output:")
    print(f"{DEST_DIR}/")
    print("├── images/")
    print("│   ├── train/")
    print("│   │   ├── nama_kelas1/ (berisi gambar .jpg, .png, dll.)")
    print("│   │   └── nama_kelas2/")
    print("│   └── val/")
    print("│       ├── nama_kelas1/")
    print("│       └── nama_kelas2/")
    print("└── labels/")
    print("    ├── train/")
    print("    │   ├── nama_kelas1/ (berisi label .txt)")
    print("    │   └── nama_kelas2/")
    print("    └── val/")
    print("        ├── nama_kelas1/")
    print("        └── nama_kelas2/")

if __name__ == '__main__':
    # Langsung panggil fungsi karena SOURCE_DIR dan DEST_DIR sudah diatur di atas
    print(f"DEBUG: Memanggil split_data_and_labels() dengan SOURCE_DIR='{SOURCE_DIR}' dan DEST_DIR='{DEST_DIR}'")
    
    # Tambahkan pengecekan apakah SOURCE_DIR benar-benar ada sebelum memanggil fungsi
    if not os.path.isdir(SOURCE_DIR):
        print(f"ERROR FATAL: Direktori sumber '{SOURCE_DIR}' yang dikonfigurasi tidak ditemukan. Mohon periksa kembali path.")
    else:
        split_data_and_labels()