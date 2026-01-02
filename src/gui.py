# src/gui.py
import sys
import os
import cv2
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from datetime import datetime
import threading

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.recognizer import process_frame
from src.tts import speak

BG = "#121212"
PANEL = "#1e1e1e"
ACCENT = "#00c853"
TEXT = "#ffffff"


class AbsensiGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Absensi Wajah Otomatis")
        self.root.geometry("1200x720")
        self.root.configure(bg=BG)

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        if not self.cap.isOpened():
            messagebox.showerror("Error", "Kamera tidak dapat dibuka")
            root.destroy()
            return

        self.running = True
        self.flip_camera = False
        self.frame_count = 0
        self.last_result = None
        self.already_recorded = set()

        self.build_layout()
        self.update_frame()

    # ======================================================
    # LAYOUT
    # ======================================================
    def build_layout(self):
        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True, padx=15, pady=15)

        cam_frame = tk.Frame(container, bg=BG)
        cam_frame.pack(side="left", fill="both", expand=True)

        self.camera_label = tk.Label(cam_frame, bg="black")
        self.camera_label.pack(fill="both", expand=True)

        side = tk.Frame(container, width=330, bg=PANEL)
        side.pack(side="right", fill="y")

        self.lbl_name = self.make_label(side)
        self.lbl_status = self.make_label(side)
        self.lbl_conf = self.make_label(side)
        self.lbl_time = self.make_label(side)

        self.build_buttons(side)

    def make_label(self, parent):
        lbl = tk.Label(parent, text="-", bg=PANEL, fg=TEXT, font=("Segoe UI", 12))
        lbl.pack(anchor="w", padx=20, pady=5)
        return lbl

    # ======================================================
    # BUTTONS
    # ======================================================
    def build_buttons(self, parent):
        frame = tk.Frame(parent, bg=PANEL)
        frame.pack(pady=15, fill="x")

        ttk.Button(frame, text="➕ Tambah Dataset", command=self.add_dataset)\
            .pack(fill="x", padx=20, pady=5)

        ttk.Button(frame, text="🔁 Flip Kamera", command=self.toggle_flip)\
            .pack(fill="x", padx=20, pady=5)

        ttk.Button(frame, text="✖ Keluar", command=self.on_close)\
            .pack(fill="x", padx=20, pady=5)

    # ======================================================
    # CAMERA LOOP
    # ======================================================
    def update_frame(self):
        if not self.running:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.root.after(15, self.update_frame)
            return

        if self.flip_camera:
            frame = cv2.flip(frame, 1)

        self.frame_count += 1

        if self.frame_count % 5 == 0:
            frame, result = process_frame(frame)
            self.last_result = result
        else:
            result = self.last_result

        if result:
            name = result["name"]
            status = result["status"]
            conf = result["confidence"]
            time_txt = result["time"]
            x1, y1, x2, y2 = result["box"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            self.lbl_name.config(text=f"Nama   : {name}")
            self.lbl_status.config(text=f"Status : {status}")
            self.lbl_conf.config(text=f"Skor   : {conf}")
            self.lbl_time.config(text=f"Waktu  : {time_txt}")

            if status == "Hadir" and name not in self.already_recorded:
                self.already_recorded.add(name)
                speak(f"Halo {name}, absensi Anda telah dicatat")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(img)

        self.camera_label.imgtk = imgtk
        self.camera_label.configure(image=imgtk)

        self.root.after(15, self.update_frame)

    # ======================================================
    # DATASET
    # ======================================================
    def add_dataset(self):
        name = simpledialog.askstring("Dataset", "Masukkan nama:")
        if not name:
            return

        self.running = False
        self.cap.release()

        t = threading.Thread(target=self.capture_dataset, args=(name,))
        t.start()

    def capture_dataset(self, name):
        DATASET_DIR = os.path.join(ROOT_DIR, "dataset", name)
        os.makedirs(DATASET_DIR, exist_ok=True)

        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        count = 0
        MAX_IMG = 30

        while count < MAX_IMG:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (160, 160))
                cv2.imwrite(f"{DATASET_DIR}/{count}.jpg", face)
                count += 1

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(frame, f"{count}/{MAX_IMG}", (10,30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            cv2.imshow("Ambil Dataset - Tekan Q untuk keluar", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.running = True
        self.update_frame()

    # ======================================================
    # UTIL
    # ======================================================
    def toggle_flip(self):
        self.flip_camera = not self.flip_camera

    def on_close(self):
        self.running = False
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AbsensiGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
