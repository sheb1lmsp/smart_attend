# Generated by Django 5.2 on 2025-05-03 13:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_student_name_remove_teacher_name_student_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='parent_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='parent_phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Phone number must be 10 digits.')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Phone number must be 10 digits.')]),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Phone number must be 10 digits.')]),
        ),
    ]
