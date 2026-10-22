# student_system/courses/models.py

# import models from django.db module for database operations
from django.db import models
# import User from django.contrib.auth.models module for user authentication and authorization
from django.contrib.auth.models import User
# import reverse from django.urls module for URL reversal
from django.urls import reverse

# define the course model to store course information
# Course class inherits from models.Model class which provides all the functionality of a Django model
# and makes it possible to work with the database
class Course(models.Model):
    """Model to store course information"""
    
    # define level choices for the course
    LEVEL_CHOICES = [
        ('100', 'Beginner'),
        ('200', 'Intermediate'),
        ('300', 'Advanced'),
        ('400', 'Expert'),
    ]
    # define status choices for the course
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ARCHIVED', 'Archived'),
    ]
    
    code = models.CharField(max_length=10, unique=True, help_text="Course Code (e.g., CS101)")
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taught_courses')
    credits = models.PositiveIntegerField(help_text="Credit hours for this course")
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES)
    capacity = models.PositiveIntegerField(help_text="Maximum number of students")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # meta class is used to define the metadata of the model, such as the ordering, verbose_name_plural, and indexes.
    class Meta:
        ordering = ['code']
        verbose_name_plural = "Courses"
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status']),
        ]

    # __str__ method is used to return the string representation of the model
    # it is used to display the string representation of the model in the admin interface and in the shell
    def __str__(self):
        return f"{self.code} - {self.title}"

    # get_absolute_url method is used to return the URL of the model
    # it is used to display the URL of the model in the admin interface and in the shell
    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'pk': self.pk})
    
    # is_available property is used to check if the course is currently available for enrollment
    # @property decorator is used to define a property method that can be accessed as an attribute of the model
    # it is used to check if the course is currently available for enrollment
    @property
    def is_available(self):
        """Check if course is currently available for enrollment"""
        return self.status == 'ACTIVE'
