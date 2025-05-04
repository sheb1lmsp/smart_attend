import os
import cv2
import torch
from facenet_pytorch import MTCNN
from pathlib import Path


def detect_faces(image_path, output_dir, j=None):

    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    mtcnn = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu')

    boxes, _ = mtcnn.detect(img_rgb)
    detected_faces = []

    if j is not None:
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = [int(b) for b in box]
            face = img[y1:y2, x1:x2]
            face_filename = output_dir / f'face_{j}_{i+1}.jpg'
            cv2.imwrite(str(face_filename), face)
    else:
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = [int(b) for b in box]
            face = img[y1:y2, x1:x2]
            face_filename = output_dir / f'face_{i+1}.jpg'
            cv2.imwrite(str(face_filename), face)
            detected_faces.append(((x1, y1, x2, y2), face_filename))
        print(f"{i+1} students are present")
        return detected_faces
