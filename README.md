# Project Absensi (Face Recognition Attendance System)

Sistem absensi berbasis pengenalan wajah menggunakan **FaceNet (facenet-pytorch)** dengan antarmuka GUI sederhana (Tkinter). Projekt ini memudahkan perekaman, pelatihan, dan pengenalan wajah untuk tujuan absensi.

---

## Fitur
- Deteksi wajah real-time dari kamera
- Identifikasi menggunakan FaceNet embeddings
- Sistem absensi otomatis dengan mekanisme cooldown untuk mencegah duplikasi
- GUI interaktif (Tkinter)
- Bounding box dan label nama pada frame video
- Text-to-Speech (sapaan/konfirmasi)

## Teknologi & Ketergantungan
- **Python 3.10**
- OpenCV
- facenet-pytorch (FaceNet)
- PyTorch
- scikit-learn
- Tkinter

> Semua dependensi tersedia di `requirements.txt`.

---

## Struktur Proyek (ringkasan)
- `src/`
  - `capture_dataset.py` — tangkap foto/record wajah untuk dataset
  - `train_dl.py` — latih model / hitung embeddings
  - `recognizer.py` — skrip pengenalan wajah (non-GUI)
  - `gui.py` — antarmuka GUI utama untuk absensi
  - `face_embedder.py` — utilitas untuk membuat embeddings
  - `database.py` — penyimpanan data absensi
  - `tts.py` — Text-to-Speech
- `dataset/` — folder dataset (subfolder per orang)
- `models/` — model dan embeddings (`embeddings.npz`)
- `audio/`, `logs/` — aset lainnya

---

## Instalasi & Persiapan
1. Aktifkan virtual environment (Windows PowerShell):

```powershell
& .\san.venv\Scripts\Activate.ps1
```

2. Install dependensi:

```bash
pip install -r requirements.txt
```

3. Pastikan kamera berfungsi dan Anda memiliki folder `dataset/` untuk menyimpan data wajah.

---

## Cara Penggunaan (singkat)
- Menangkap data wajah (untuk satu pengguna):

```bash
python src\capture_dataset.py --name "NamaAnda"
```

- Melatih / memperbarui embeddings:

```bash
python src\train_dl.py
```

- Menjalankan GUI absensi:

```bash
python src\gui.py
```

- Menjalankan pengenalan wajah lewat terminal (opsional):

```bash
python src\recognizer.py
```

---

## Tips & Catatan
- Letakkan folder dataset dengan nama user (mis. `dataset/Hasan`) berisi beberapa foto wajah untuk hasil terbaik.
- `models/embeddings.npz` menyimpan embeddings yang dihasilkan oleh proses training.
---