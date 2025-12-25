# src/face_embedder.py
import torch
import cv2
import numpy as np
from facenet_pytorch import MTCNN, InceptionResnetV1

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

mtcnn = MTCNN(
    image_size=160,
    margin=10,
    keep_all=False,
    min_face_size=80,
    device=device
)

model = InceptionResnetV1(pretrained="vggface2").eval().to(device)


def detect_face_box(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, _ = mtcnn.detect(rgb)
    if boxes is None:
        return None

    box = boxes[0]
    return tuple(map(int, box))


def get_embedding(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face = mtcnn(rgb)
    if face is None:
        return None

    face = face.unsqueeze(0).to(device)

    with torch.no_grad():
        emb = model(face)

    return emb.cpu().numpy()[0]
