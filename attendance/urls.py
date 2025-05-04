from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('student_dashboard/', views.student_dashboard, name="student_dashboard"),
    path('teacher_dashboard/', views.teacher_dashboard, name="teacher_dashboard"),
    path('subject_class_detail/<int:subject_id>/<int:class_id>/', views.subject_class_detail, name='subject_class_detail'),
    path('mark_attendance/<int:subject_id>/<int:class_id>/', views.mark_attendance, name='mark_attendance'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)