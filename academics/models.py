from django.db import models
from django.conf import settings


class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=100)
    credits = models.PositiveIntegerField()
    department = models.ForeignKey('students.Department', on_delete=models.CASCADE,
                                   related_name='courses')
    semester_offered = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['course_code']

    def __str__(self):
        return f'{self.course_code} - {self.course_name}'


class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='subjects')
    code = models.CharField(max_length=20)
    theory_marks = models.PositiveIntegerField(default=70)
    practical_marks = models.PositiveIntegerField(default=30)
    class_meta = models.TextField(blank=True)

    class Meta:
        unique_together = ['course', 'code']
        ordering = ['code']

    def __str__(self):
        return f'{self.code} - {self.name}'


class Enrollment(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE,
                                related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='enrollments')
    academic_year = models.CharField(max_length=10)
    semester = models.PositiveIntegerField()
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='active',
                              choices=[('active', 'Active'), ('dropped', 'Dropped'), ('completed', 'Completed')])

    class Meta:
        unique_together = ['student', 'course', 'academic_year', 'semester']
        ordering = ['academic_year', 'semester']

    def __str__(self):
        return f'{self.student.enrollment_number} - {self.course.course_code}'
