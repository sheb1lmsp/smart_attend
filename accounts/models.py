from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    student_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits.')]
    )
    parent_name = models.CharField(max_length=50)
    parent_phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits.')]
    )
    class_batch = models.ForeignKey('training.Class', on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    teacher_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits.')]
    )
    classes = models.ManyToManyField('training.Class')
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.user.username