from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin interface for Course model"""
    
    list_display = ['code', 'title', 'get_instructor_name', 'level', 'capacity', 'status', 'start_date']
    list_filter = ['status', 'level', 'start_date']
    search_fields = ['code', 'title', 'instructor__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Course Information', {
            'fields': ('code', 'title', 'description')
        }),
        ('Course Details', {
            'fields': ('instructor', 'credits', 'level', 'capacity', 'status')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_instructor_name(self, obj):
        """Display instructor name"""
        if obj.instructor:
            return obj.instructor.get_full_name() or obj.instructor.username
        return 'N/A'
    get_instructor_name.short_description = 'Instructor'
