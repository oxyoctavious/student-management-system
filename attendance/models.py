from django.db import models
from django.conf import settings


class AttendanceSession(models.Model):
    enrollment = models.ForeignKey('academics.Enrollment', on_delete=models.CASCADE,
                                   related_name='attendance_sessions')
    date = models.DateField()
    is_conducted = models.BooleanField(default=False)
    conducted_by = models.ForeignKey('staff.Staff', on_delete=models.SET_NULL,
                                     null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['enrollment', 'date']
        ordering = ['-date']

    def __str__(self):
        return f'{self.enrollment} - {self.date}'


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE,
                                related_name='records')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE,
                                related_name='attendance_records')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    remarks = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['session', 'student']

    def __str__(self):
        return f'{self.student.enrollment_number} - {self.session.date} - {self.status}'


class AttendanceSummary(models.Model):
    enrollment = models.ForeignKey('academics.Enrollment', on_delete=models.CASCADE,
                                   related_name='attendance_summary')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE,
                                related_name='attendance_summaries')
    total_classes = models.PositiveIntegerField(default=0)
    present_classes = models.PositiveIntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['enrollment', 'subject']

    def __str__(self):
        return f'{self.enrollment.student.enrollment_number} - {self.subject.code} - {self.percentage}%'
