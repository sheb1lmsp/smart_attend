# Generated by Django 5.2 on 2025-05-01 11:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_initial'),
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present_or_not', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('period', models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6)], max_length=1)),
                ('class_batch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='training.class')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.subject')),
                ('taken_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.teacher')),
                ('attendance_report', models.ManyToManyField(to='attendance.attendancereport')),
            ],
        ),
    ]
