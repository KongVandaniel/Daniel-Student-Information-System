from django.db import models
from students.models import Student
from courses.models import Course
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Enrollment(models.Model):
    """Model to store student course enrollment information"""
    
    STATUS_CHOICES = [
        ('ENROLLED', 'Enrolled'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped'),
        ('SUSPENDED', 'Suspended'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ENROLLED')
    grade = models.CharField(max_length=2, blank=True, null=True, help_text="Letter grade (A, B, C, D, F)")
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrollment_date']
        verbose_name_plural = "Enrollments"
        indexes = [
            models.Index(fields=['student', 'course']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.student.student_id} - {self.course.code}"

    def get_absolute_url(self):
        return reverse('enrollments:enrollment_detail', kwargs={'pk': self.pk})

    def calculate_grade(self):
        """Calculate letter grade based on score"""
        if self.score is None:
            return None
        
        if self.score >= 90:
            return 'A'
        elif self.score >= 80:
            return 'B'
        elif self.score >= 70:
            return 'C'
        elif self.score >= 60:
            return 'D'
        else:
            return 'F'
    
    def save(self, *args, **kwargs):
        """Automatically calculate grade before saving"""
        if self.score and not self.grade:
            self.grade = self.calculate_grade()
        super().save(*args, **kwargs)
