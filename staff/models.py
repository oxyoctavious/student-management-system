from django.db import models
from django.conf import settings


class Staff(models.Model):
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('lab_assistant', 'Lab Assistant'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='staff_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey('students.Department', on_delete=models.CASCADE,
                                   related_name='staff_members')
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    qualification = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=15, blank=True)
    date_of_joining = models.DateField(auto_now_add=True)
    is_active_staff = models.BooleanField(default=True)

    class Meta:
        ordering = ['employee_id']

    def __str__(self):
        return f'{self.employee_id} - {self.user.first_name} {self.user.last_name}'
