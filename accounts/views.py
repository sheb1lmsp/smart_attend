from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .models import Student, Teacher


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                is_student = Student.objects.filter(user=user).exists()
                is_teacher = Teacher.objects.filter(user=user).exists()
            except (Student.DoesNotExist, Teacher.DoesNotExist):
                is_student, is_teacher = False, False

            if user_type == 'student' and is_student:
                login(request, user)
                return redirect('student_dashboard')
            elif user_type == 'teacher' and is_teacher:
                login(request, user)
                return redirect('teacher_dashboard')
            elif user_type == 'student':
                messages.error(request, "You are not registered as a student.")
            elif user_type == 'teacher':
                messages.error(request, "You are not registered as a teacher.")
            else:
                messages.error(request, "Please select a valid user type.")
        else:
            messages.error(request, "Invalid username or password.")

        return render(request, 'login.html', {
            'username': username,
            'user_type': user_type,
        })
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def student_required(view_func):
    return user_passes_test(
        lambda user: Student.objects.filter(user=user).exists(),
        login_url='/login/',
        redirect_field_name=None
    )(view_func)


def teacher_required(view_func):
    return user_passes_test(
        lambda user: Teacher.objects.filter(user=user).exists(),
        login_url='/login/',
        redirect_field_name=None
    )(view_func)