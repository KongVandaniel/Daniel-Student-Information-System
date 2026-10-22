from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    """Model to store student information"""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_id = models.CharField(max_length=20, unique=True, help_text="Unique Student ID")
    khmer_name = models.CharField(
        max_length=150, 
        blank=True, 
        default='', 
        verbose_name="Khmer Name", 
        help_text="ឈ្មោះជាភាសាខ្មែរ (e.g. ពេជ្រ វល័ក្ខ)"
    )
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    enrollment_date = models.DateField(auto_now_add=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0, 
                              validators=[MinValueValidator(0), MaxValueValidator(4)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_id']
        verbose_name_plural = "Students"
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['user']),
            models.Index(fields=['khmer_name']),
        ]

    def get_primary_name(self):
        """Return Khmer name as primary; fall back to User full name or username"""
        if self.khmer_name:
            return self.khmer_name
        full_name = self.user.get_full_name()
        return full_name if full_name else self.user.username

    def __str__(self):
        return f"{self.student_id} - {self.get_primary_name()}"

    def get_absolute_url(self):
        return reverse('students:student_detail', kwargs={'pk': self.pk})

