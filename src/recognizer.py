# src/recognizer.py
import os
import time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from face_embedder import get_embedding, detect_face_box

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMB_PATH = os.path.join(BASE_DIR, "models", "embeddings.npz")

THRESHOLD = 0.35           # cosine similarity
COOLDOWN_TIME = 10         # detik
PROCESS_INTERVAL = 0.3     # detik (anti lag)

db_embeddings = None
db_names = None

last_process_time = 0
last_seen_name = None
last_seen_time = 0


def load_database():
    global db_embeddings, db_names
    if os.path.exists(EMB_PATH):
        data = np.load(EMB_PATH, allow_pickle=True)
        db_embeddings = data["embeddings"]
        db_names = data["names"]
        print("[INFO] Database embedding dimuat")
    else:
        db_embeddings = None
        db_names = None
        print("[WARN] Database embedding belum ada")


load_database()


def process_frame(frame):
    global last_process_time, last_seen_name, last_seen_time

    now = time.time()
    if now - last_process_time < PROCESS_INTERVAL:
        return frame, None

    last_process_time = now

    if db_embeddings is None:
        return frame, None

    # DETEKSI WAJAH (bounding box)
    box = detect_face_box(frame)
    if box is None:
        return frame, None

    x1, y1, x2, y2 = box

    emb = get_embedding(frame)
    if emb is None:
        return frame, None

    sims = cosine_similarity([emb], db_embeddings)[0]
    best_idx = np.argmax(sims)
    best_score = sims[best_idx]

    if best_score >= THRESHOLD:
        name = str(db_names[best_idx])
        status = "Hadir"
    else:
        name = "Unknown"
        status = "Tidak dikenal"

    # COOLDOWN ABSENSI
    if name != "Unknown":
        if name == last_seen_name and now - last_seen_time < COOLDOWN_TIME:
            status = "Cooldown"
        else:
            last_seen_name = name
            last_seen_time = now

    result = {
        "name": name,
        "status": status,
        "confidence": round(float(best_score), 2),
        "time": time.strftime("%H:%M:%S"),
        "box": (x1, y1, x2, y2)
    }

    return frame, result
