from django.db import models


class AttendanceReport(models.Model):
    student = models.ForeignKey('accounts.Student', on_delete=models.PROTECT)
    present_or_not = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} is {'present' if self.present_or_not else 'absent'}"


class Attendance(models.Model):
    CHOICES = [
        ('1', 'Period 1'),
        ('2', 'Period 2'),
        ('3', 'Period 3'),
        ('4', 'Period 4'),
        ('5', 'Period 5'),
        ('6', 'Period 6'),
    ]
    class_batch = models.ForeignKey('training.Class', on_delete=models.PROTECT)
    taken_by = models.ForeignKey('accounts.Teacher', on_delete=models.PROTECT)
    date = models.DateField()
    period = models.CharField(max_length=1, choices=CHOICES)
    subject = models.ForeignKey('accounts.Subject', on_delete=models.PROTECT)
    attendance_report = models.ManyToManyField(AttendanceReport)

    class Meta:
        unique_together = ('class_batch', 'date', 'period', 'subject')

    def __str__(self):
        return f"{self.class_batch.department}_{self.class_batch.batch}_{self.period}"