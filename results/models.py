from django.db import models
from django.conf import settings


class Exam(models.Model):
    EXAM_TYPES = [
        ('mid_term', 'Mid Term'),
        ('final', 'Final Exam'),
        ('practical', 'Practical'),
        ('internal', 'Internal Assessment'),
    ]

    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE,
                               related_name='exams')
    semester = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=10)
    total_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=40)
    exam_date = models.DateField()
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-exam_date']

    def __str__(self):
        return f'{self.name} - {self.course.course_code}'


class Result(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+ (90-100)'),
        ('A', 'A (80-89)'),
        ('B', 'B (70-79)'),
        ('C', 'C (60-69)'),
        ('D', 'D (50-59)'),
        ('E', 'E (40-49)'),
        ('F', 'F (Below 40)'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,
                             related_name='results')
    enrollment = models.ForeignKey('academics.Enrollment', on_delete=models.CASCADE,
                                   related_name='exam_results')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE,
                                related_name='results')
    theory_marks = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    practical_marks = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_marks_obtained = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, default='F')
    remarks = models.TextField(blank=True)
    is_passed = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['exam', 'enrollment', 'subject']
        ordering = ['enrollment', 'subject']

    def __str__(self):
        return f'{self.enrollment.student.enrollment_number} - {self.subject.code} - {self.grade}'


class SemesterResult(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE,
                                related_name='semester_results')
    semester = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=10)
    total_credits = models.PositiveIntegerField(default=0)
    earned_credits = models.PositiveIntegerField(default=0)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    sgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    overall_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, default='in_progress',
                              choices=[('in_progress', 'In Progress'), ('passed', 'Passed'), ('failed', 'Failed')])
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'semester', 'academic_year']
        ordering = ['academic_year', 'semester']

    def __str__(self):
        return f'{self.student.enrollment_number} - Sem {self.semester} - {self.sgpa}'
