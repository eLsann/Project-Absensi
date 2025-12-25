import os
import cv2
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)
    
import numpy as np
from src.face_embedder import get_embedding

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "embeddings.npz")

os.makedirs(MODEL_DIR, exist_ok=True)

embeddings = []
names = []

print("[INFO] Training embedding dimulai...")

for person in os.listdir(DATASET_DIR):
    person_dir = os.path.join(DATASET_DIR, person)
    if not os.path.isdir(person_dir):
        continue

    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)
        img = cv2.imread(img_path)

        if img is None:
            continue

        emb = get_embedding(img)
        if emb is None:
            continue

        embeddings.append(emb)
        names.append(person)

if len(embeddings) == 0:
    raise RuntimeError("Dataset kosong atau wajah tidak terdeteksi")

np.savez(
    MODEL_PATH,
    embeddings=np.array(embeddings),
    names=np.array(names)
)

print("[INFO] Training selesai. Model tersimpan.")
