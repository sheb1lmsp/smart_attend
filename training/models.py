from django.db import models
from django.core.validators import RegexValidator


class Class(models.Model):
    department = models.ForeignKey('accounts.Department', on_delete=models.PROTECT)
    batch = models.CharField(
        max_length=4,
        validators=[RegexValidator(r'^\d{4}$', 'Batch must be a 4-digit year (e.g., 2023).')]
    )
    subjects = models.ManyToManyField('accounts.Subject')

    class Meta:
        unique_together = ['department', 'batch']

    def __str__(self):
        return f"{self.department.name}_{self.batch}"