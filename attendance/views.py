from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.views import student_required, teacher_required
from training.models import Class
from attendance.models import Attendance, AttendanceReport
from accounts.models import Student, Subject, Teacher
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta
import os
from django.conf import settings
from modules.model import create_model
from modules.recognition import recognition
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import torch
from django.core.exceptions import ObjectDoesNotExist
import tempfile
from django.core.exceptions import ValidationError


FACES_DIR = Path(settings.MEDIA_ROOT) / 'faces'
MODELS_DIR = Path(settings.MEDIA_ROOT) / 'models'
UPLOAD_DIR = Path(settings.MEDIA_ROOT) / 'uploads'


os.makedirs(FACES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)


@login_required
@student_required
def student_dashboard(request):
    student = request.user.student
    class_batch = student.class_batch
    subjects = class_batch.subjects.all()

    # Get all attendance reports for the student
    attendance_reports = AttendanceReport.objects.filter(
        student=student
    ).select_related('student')
    total_classes = attendance_reports.count()
    present_classes = attendance_reports.filter(present_or_not=True).count()
    attendance_percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0

    # Subject-wise attendance statistics
    subject_stats = []
    for subject in subjects:
        subject_reports = AttendanceReport.objects.filter(
            student=student,
            attendance__in=Attendance.objects.filter(
                class_batch=class_batch,
                subject=subject
            )
        )
        total = subject_reports.count()
        present = subject_reports.filter(present_or_not=True).count()
        percentage = (present / total * 100) if total > 0 else 0
        subject_stats.append({
            'subject': subject,
            'total': total,
            'present': present,
            'percentage': round(percentage, 2)
        })

    # Complete attendance history
    all_attendance = Attendance.objects.filter(
        class_batch=class_batch,
        attendance_report__student=student
    ).prefetch_related('attendance_report', 'subject', 'taken_by').order_by('-date')

    context = {
        'student': student,
        'class_batch': class_batch,
        'subjects': subjects,
        'attendance_percentage': round(attendance_percentage, 2),
        'total_classes': total_classes,
        'present_classes': present_classes,
        'subject_stats': subject_stats,
        'all_attendance': all_attendance,
    }

    return render(request, 'student_dashboard.html', context)


@login_required
@teacher_required
def teacher_dashboard(request):
    teacher = request.user.teacher
    subjects = teacher.subjects.all()
    classes = teacher.classes.all()

    # Prepare subject-class combination data
    subject_class_data = []
    for subject in subjects:
        subject_classes = classes.filter(subjects=subject)
        for class_batch in subject_classes:
            students = Student.objects.filter(class_batch=class_batch)
            total_sessions = Attendance.objects.filter(
                taken_by=teacher,
                subject=subject,
                class_batch=class_batch
            ).count()
            subject_class_data.append({
                'subject': subject,
                'class_batch': class_batch,
                'student_count': students.count(),
                'total_sessions': total_sessions,
            })

    context = {
        'teacher': teacher,
        'subject_class_data': subject_class_data,
    }

    return render(request, 'teacher_dashboard.html', context)


@login_required
@teacher_required
def subject_class_detail(request, subject_id, class_id):
    teacher = request.user.teacher
    subject = get_object_or_404(Subject, id=subject_id, teacher=teacher)
    class_batch = get_object_or_404(Class, id=class_id, teacher=teacher, subjects=subject)

    # Get students enrolled in the class
    students = Student.objects.filter(class_batch=class_batch).select_related('user').order_by('user__username')

    # Get attendance records for the subject and class taken by the teacher
    attendance_sessions = Attendance.objects.filter(
        taken_by=teacher,
        subject=subject,
        class_batch=class_batch
    ).select_related('class_batch').order_by('date', 'period')[:10]

    # Get attendance data
    attendance_data = []
    for student in students:
        student_data = {
            'student': student,
            'sessions': [],
            'total_classes': 0,
            'present_classes': 0,
        }
        for session in attendance_sessions:
            attendance = AttendanceReport.objects.filter(
                attendance=session,
                student=student
            ).first()
            present = attendance.present_or_not if attendance else False
            student_data['sessions'].append({
                'session': session,
                'present': present,
            })
            student_data['total_classes'] += 1
            if present:
                student_data['present_classes'] += 1
        attendance_percentage = (
            (student_data['present_classes'] / student_data['total_classes'] * 100)
            if student_data['total_classes'] > 0 else 0
        )
        student_data['attendance_percentage'] = round(attendance_percentage, 2)
        attendance_data.append(student_data)

    context = {
        'subject': subject,
        'class_batch': class_batch,
        'students': students,
        'attendance_sessions': attendance_sessions,
        'attendance_data': attendance_data,
    }

    return render(request, 'subject_class_detail.html', context)


@login_required
@teacher_required
def mark_attendance(request, subject_id, class_id):
    teacher = request.user.teacher

    try:
        class_batch = Class.objects.get(id=class_id)
        subject = Subject.objects.get(id=subject_id)

        # Verify teacher is authorized
        if not (class_batch in teacher.classes.all() and subject in teacher.subjects.all()):
            messages.error(request, "You are not authorized to mark attendance for this class or subject.")
            return redirect('subject_class_detail', subject_id=subject_id, class_id=class_id)

        if request.method == 'POST':
            period = request.POST.get('period')
            image = request.FILES.get('group_photo')

            # Validate file type
            if not image.content_type.startswith('image/'):
                messages.error(request, "Please upload a valid image file.")
                return redirect('mark_attendance', subject_id=subject_id, class_id=class_id)

            # Check if attendance already exists
            current_date = timezone.now().date()
            if Attendance.objects.filter(
                class_batch=class_batch,
                date=current_date,
                period=period,
                subject=subject
            ).exists():
                messages.error(request, "Attendance for this class, date, period, and subject has already been marked.")
                return redirect('subject_class_detail', subject_id=subject_id, class_id=class_id)

            # Load the trained model
            model_path = MODELS_DIR / str(class_batch) / f"{str(class_batch)}.pth"
            class_names_path = MODELS_DIR / str(class_batch) / f"{str(class_batch)}_class_names.txt"

            if not model_path.exists() or not class_names_path.exists():
                messages.error(request, "Model or class names file not found.")
                return redirect('mark_attendance', subject_id=subject_id, class_id=class_id)

            try:
                class_names = []
                with class_names_path.open('r') as f:
                    class_names = [line.strip() for line in f if line.strip()]

                loaded_state_dict = torch.load(model_path, map_location=torch.device('cpu'))
                model = create_model(len(class_names), device="cpu")
                model.load_state_dict(loaded_state_dict)

                # Get students for the class
                students = Student.objects.filter(class_batch=class_batch).select_related('user')

                # Save uploaded image temporarily and define output path
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_image_path = Path(temp_dir) / 'group_photo.jpg'
                    fs = FileSystemStorage(location=temp_dir)
                    filename = fs.save('group_photo.jpg', image)
                    temp_image_path = Path(temp_dir) / filename

                    # Define output path for processed image
                    output_filename = f"processed_{class_batch}_{current_date}_{period}.jpg"
                    output_image_path = UPLOAD_DIR / output_filename

                    # Run face recognition and save processed image
                    attendance_results = recognition(temp_image_path, FACES_DIR, class_names, model, output_image_path)

                    # Create Attendance record with current date
                    attendance = Attendance.objects.create(
                        class_batch=class_batch,
                        taken_by=teacher,
                        date=current_date,
                        period=period,
                        subject=subject
                    )

                    # Create AttendanceReport records
                    for student in students:
                        report = AttendanceReport.objects.create(
                            student=student,
                            present_or_not=attendance_results.get(student.user.username, False)
                        )
                        attendance.attendance_report.add(report)

                    # Generate URL for processed image
                    processed_image_url = f"{settings.MEDIA_URL}uploads/{output_filename}"

                    messages.success(request, "Attendance marked successfully.")
                    # Render the same template with the processed image
                    context = {
                        'class_batch': class_batch,
                        'subject': subject,
                        'periods': Attendance.CHOICES,
                        'current_date': current_date,
                        'processed_image_url': processed_image_url,
                    }
                    return render(request, 'mark_attendance.html', context)

            except Exception as e:
                messages.error(request, f"Error processing attendance: {str(e)}")
                return redirect('mark_attendance', subject_id=subject_id, class_id=class_id)

    except ObjectDoesNotExist:
        messages.error(request, "Invalid class or subject selected.")
        return redirect('teacher_dashboard')

    # GET request - show form
    periods = Attendance.CHOICES

    context = {
        'class_batch': class_batch,
        'subject': subject,
        'periods': periods,
        'current_date': timezone.now().date(),
    }
    return render(request, 'mark_attendance.html', context)