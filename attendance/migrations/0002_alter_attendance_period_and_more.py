# Generated by Django 5.2 on 2025-05-03 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_department_name_alter_subject_name'),
        ('attendance', '0001_initial'),
        ('training', '0002_remove_class_trained_model_alter_class_batch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='period',
            field=models.CharField(choices=[('1', 'Period 1'), ('2', 'Period 2'), ('3', 'Period 3'), ('4', 'Period 4'), ('5', 'Period 5'), ('6', 'Period 6')], max_length=1),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('class_batch', 'date', 'period', 'subject')},
        ),
    ]
