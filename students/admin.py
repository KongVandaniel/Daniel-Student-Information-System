from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin interface for Student model"""
    
    list_display = ['student_id', 'khmer_name', 'get_full_name', 'gender', 'city', 'gpa', 'is_active', 'enrollment_date']
    list_filter = ['is_active', 'gender', 'city', 'enrollment_date']
    search_fields = ['student_id', 'khmer_name', 'user__username', 'user__first_name', 'user__last_name', 'user__email']
    readonly_fields = ['enrollment_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User & Identity Information', {
            'fields': ('user', 'student_id', 'khmer_name')
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'gender', 'phone_number', 'profile_picture')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'country')
        }),
        ('Academic Information', {
            'fields': ('gpa', 'is_active')
        }),
        ('Dates', {
            'fields': ('enrollment_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        """Display full name from related User"""
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
