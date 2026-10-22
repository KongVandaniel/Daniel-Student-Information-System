from django.shortcuts import render
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment

def home(request):
    """Home page with system statistics"""
    context = {
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
        'active_students': Student.objects.filter(is_active=True).count(),
        'active_courses': Course.objects.filter(status='ACTIVE').count(),
    }
    return render(request, 'home.html', context)
