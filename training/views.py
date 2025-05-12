from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.conf import settings
from accounts.views import student_required, teacher_required
from accounts.models import Teacher, Student
from .models import Class
from modules.face_detection import detect_faces
from modules.train import train
from pathlib import Path
import os
import glob
from django.contrib import messages
import re


# Define paths
UPLOAD_DIR = Path(settings.MEDIA_ROOT) / 'uploads'
FACES_DIR = Path(settings.MEDIA_ROOT) / 'faces'
MODELS_DIR = Path(settings.MEDIA_ROOT) / 'models'
TRAIN_DIR = Path(settings.MEDIA_ROOT) / 'train'


# Ensure base directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FACES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(TRAIN_DIR, exist_ok=True)


@login_required
@teacher_required
def detect_faces_view(request, class_id):
    teacher = request.user.teacher
    class_obj = get_object_or_404(Class, id=class_id)
    if not teacher.classes.filter(id=class_id).exists():
        messages.error(request, "You are not assigned to this class.")
        return render(request, 'error.html', {'message': 'You are not assigned to this class.', 'class_id': class_id})

    # Define class-specific directories
    batch_name = re.sub(r'[^\w\-]', '_', str(class_obj))  # Sanitize batch name
    class_upload_dir = UPLOAD_DIR / batch_name
    class_faces_dir = FACES_DIR / batch_name
    os.makedirs(class_upload_dir, exist_ok=True)
    os.makedirs(class_faces_dir, exist_ok=True)

    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('images')
        if not uploaded_files:
            messages.error(request, "Please upload at least one image.")
            return render(request, 'detect_faces.html', {'class_obj': class_obj})

        # Validate file types
        for file in uploaded_files:
            if not file.content_type.startswith('image/'):
                messages.error(request, f"File '{file.name}' is not a valid image.")
                return render(request, 'detect_faces.html', {'class_obj': class_obj})

        fs = FileSystemStorage(location=class_upload_dir)
        uploaded_filenames = []

        # Save uploaded images to class-specific upload directory
        for file in uploaded_files:
            filename = fs.save(file.name, file)
            uploaded_filenames.append(filename)

        # Process each uploaded image for face detection
        for idx, filename in enumerate(uploaded_filenames):
            image_path = class_upload_dir / filename
            detect_faces(image_path, class_faces_dir, j=idx)

        # Clean up uploaded images
        for filename in uploaded_filenames:
            (class_upload_dir / filename).unlink(missing_ok=True)

        messages.success(request, "Faces detected successfully.")
        return redirect('label_faces', class_id=class_id)

    return render(request, 'detect_faces.html', {'class_obj': class_obj})


@login_required
@teacher_required
def label_faces_view(request, class_id):
    teacher = request.user.teacher
    class_obj = get_object_or_404(Class, id=class_id)
    if not teacher.classes.filter(id=class_id).exists():
        messages.error(request, "You are not assigned to this class.")
        return render(request, 'error.html', {'message': 'You are not assigned to this class.', 'class_id': class_id})

    # Define class-specific faces directory
    batch_name = re.sub(r'[^\w\-]', '_', str(class_obj))  # Sanitize batch name
    class_faces_dir = FACES_DIR / batch_name
    class_train_dir = TRAIN_DIR / batch_name

    students = Student.objects.filter(class_batch=class_obj).select_related('user')
    student_names = [student.user.username for student in students] + ['Unknown']
    face_images = [Path(img).name for img in glob.glob(str(class_faces_dir / '*.jpg'))]
    selected_labels = {}
    selected_labels_map = {}  # Maps filename to selected label (e.g., {"face1.jpg": "student1"})

    if request.method == 'POST':
        # Handle form submission for labeling
        for key, label in request.POST.items():
            if key.startswith('face_') and label in student_names:
                selected_labels[key] = label
                # Store in selected_labels_map without the "face_" prefix
                filename = key.replace('face_', '', 1)
                selected_labels_map[filename] = label

        # Check for at least one valid student selection
        has_valid_selection = any(label != 'Unknown' for key, label in selected_labels.items() if key.startswith('face_'))

        if not has_valid_selection:
            messages.error(request, "Please select at least one student for labeling (excluding Unknown).")
            return render(request, 'label_faces.html', {
                'face_images': face_images,
                'student_names': student_names,
                'class_obj': class_obj,
                'selected_labels': selected_labels,
                'selected_labels_map': selected_labels_map,
                'batch_name': batch_name,
            })

        # Create class batch directory for training
        os.makedirs(class_train_dir, exist_ok=True)

        # Move labeled faces to media/train/<class_batch>/<student_username>
        for key, label in selected_labels.items():
            if key.startswith('face_') and label != 'Unknown':
                face_filename = key.replace('face_', '', 1)
                face_path = class_faces_dir / face_filename
                student_dir = class_train_dir / label
                os.makedirs(student_dir, exist_ok=True)
                os.rename(face_path, student_dir / face_filename)

        # Clean up remaining face images
        for face_image in face_images:
            (class_faces_dir / face_image).unlink(missing_ok=True)

        messages.success(request, "Faces labeled successfully.")
        return redirect('train_model', class_id=class_id)

    return render(request, 'label_faces.html', {
        'face_images': face_images,
        'student_names': student_names,
        'class_obj': class_obj,
        'selected_labels': selected_labels,
        'selected_labels_map': selected_labels_map,
        'batch_name': batch_name,
    })


@login_required
@teacher_required
def train_model_view(request, class_id):
    teacher = request.user.teacher
    class_obj = get_object_or_404(Class, id=class_id)
    if not teacher.classes.filter(id=class_id).exists():
        messages.error(request, "You are not assigned to this class.")
        return render(request, 'error.html', {'message': 'You are not assigned to this class.', 'class_id': class_id})

    # Define class-specific directories
    batch_name = re.sub(r'[^\w\-]', '_', str(class_obj))  # Sanitize batch name
    class_train_dir = TRAIN_DIR / batch_name
    class_upload_dir = UPLOAD_DIR / batch_name
    class_faces_dir = FACES_DIR / batch_name

    if not class_train_dir.exists():
        messages.error(request, "No labeled data found for this batch.")
        return render(request, 'error.html', {'message': 'No labeled data found for this batch.', 'class_id': class_id})

    # Call the train function with class-specific directory
    train_acc, train_loss = train(batch_name, str(class_train_dir))

    # Clean up images for this class
    for image in class_upload_dir.glob("*.jpg"):
        image.unlink(missing_ok=True)
    for image in class_faces_dir.glob("*.jpg"):
        image.unlink(missing_ok=True)
    for student_dir in class_train_dir.glob("*"):
        for image in student_dir.glob("*.jpg"):
            image.unlink(missing_ok=True)

    messages.success(request, f"Model for {batch_name} trained successfully.")
    return render(request, 'train_complete.html', {
        'batch_name': batch_name,
        'train_acc': train_acc,
        'train_loss': train_loss,
        'class_id': class_id,
    })