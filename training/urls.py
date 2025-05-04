from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('detect_faces/<int:class_id>/', views.detect_faces_view, name='detect_faces'),
    path('label_faces/<int:class_id>/', views.label_faces_view, name='label_faces'),
    path('train_model/<int:class_id>/', views.train_model_view, name='train_model'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)