import torch
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from modules.model import create_model
from modules.transform import create_transform
from modules.face_detection import detect_faces
import os

def recognition(image_path, face_dir, class_names, model, output_image_path):
    res = {class_name: False for class_name in class_names}

    # Detect faces and get bounding boxes with cropped face paths
    detected_faces = detect_faces(image_path, face_dir)

    # Open the original image for drawing
    original_image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(original_image)

    # Try to load a font; fall back to default if unavailable
    try:
        font = ImageFont.truetype("arial.ttf", 100)  # Increased font size
    except IOError:
        font = ImageFont.load_default()

    transform = create_transform()

    for bbox, face_path in detected_faces:
        # Process each detected face
        image = Image.open(face_path)
        transformed_image = transform(image)

        model.eval()
        with torch.inference_mode():
            y_logit = model(transformed_image.unsqueeze(dim=0))
            y_pred = torch.softmax(y_logit, dim=1)
            y_label = torch.argmax(y_pred, dim=1)
            y_class = class_names[y_label]

            res[y_class] = True

            # Draw bounding box and name
            x1, y1, x2, y2 = bbox
            draw.rectangle((x1, y1, x2, y2), outline="green", width=6)  # Green color, bolder width
            # Draw name above the bounding box
            text_position = (x1, y1 - 35 if y1 - 35 > 0 else y1)  # Adjusted for larger font
            draw.text(text_position, y_class, fill="green", font=font)  # Match text color to bounding box

        # Clean up cropped face image
        os.remove(face_path)

    # Save the processed image with bounding boxes and names
    original_image.save(output_image_path, "JPEG")

    return res