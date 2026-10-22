from django.contrib import admin
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin interface for Enrollment model"""
    
    list_display = ['get_student_id', 'get_course_code', 'status', 'grade', 'score', 'attendance_percentage', 'enrollment_date']
    list_filter = ['status', 'enrollment_date', 'grade']
    search_fields = ['student__student_id', 'course__code', 'student__user__username']
    readonly_fields = ['enrollment_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Enrollment Information', {
            'fields': ('student', 'course', 'status')
        }),
        ('Grade Information', {
            'fields': ('score', 'grade', 'attendance_percentage')
        }),
        ('Additional Information', {
            'fields': ('notes', 'completed_date')
        }),
        ('Dates', {
            'fields': ('enrollment_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_student_id(self, obj):
        """Display student ID"""
        return obj.student.student_id
    get_student_id.short_description = 'Student ID'
    
    def get_course_code(self, obj):
        """Display course code"""
        return obj.course.code
    get_course_code.short_description = 'Course Code'
