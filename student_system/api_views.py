from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment
from student_system.serializers import StudentSerializer, CourseSerializer, EnrollmentSerializer, EnrollmentDetailSerializer

class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for Student API endpoints"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['is_active', 'gender', 'city']
    search_fields = ['student_id', 'khmer_name', 'user__username', 'user__first_name', 'user__last_name']
    ordering_fields = ['student_id', 'enrollment_date', 'gpa']
    ordering = ['student_id']
    
    def perform_create(self, serializer):
        if 'user' not in serializer.validated_data:
            serializer.save(user=self.request.user)
        else:
            serializer.save()
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Get all enrollments for a specific student"""
        student = self.get_object()
        enrollments = student.enrollments.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def transcript(self, request, pk=None):
        """Get academic transcript for a student"""
        student = self.get_object()
        enrollments = student.enrollments.filter(status='COMPLETED')
        
        total_score = sum([e.score or 0 for e in enrollments if e.score])
        average_score = total_score / len(enrollments) if enrollments else 0
        
        data = {
            'student_id': student.student_id,
            'student_name': student.user.get_full_name(),
            'total_courses': student.enrollments.count(),
            'completed_courses': enrollments.count(),
            'average_score': round(average_score, 2),
            'gpa': float(student.gpa),
            'enrollments': EnrollmentDetailSerializer(enrollments, many=True).data
        }
        return Response(data)

class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course API endpoints"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_fields = ['status', 'level']
    search_fields = ['code', 'title', 'instructor__username']
    ordering_fields = ['code', 'start_date', 'capacity']
    ordering = ['code']
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Get all enrollments for a specific course"""
        course = self.get_object()
        enrollments = course.enrollments.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students enrolled in a course"""
        course = self.get_object()
        students = Student.objects.filter(enrollments__course=course).distinct()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def enrollment_statistics(self, request, pk=None):
        """Get enrollment statistics for a course"""
        course = self.get_object()
        enrollments = course.enrollments.all()
        
        data = {
            'course_code': course.code,
            'course_title': course.title,
            'total_capacity': course.capacity,
            'total_enrolled': enrollments.filter(status='ENROLLED').count(),
            'total_completed': enrollments.filter(status='COMPLETED').count(),
            'total_dropped': enrollments.filter(status='DROPPED').count(),
            'average_score': enrollments.filter(score__isnull=False).values('score').aggregate(avg=__import__('django.db.models', fromlist=['Avg']).Avg('score'))['avg'] or 0,
        }
        return Response(data)

class EnrollmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Enrollment API endpoints"""
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'student__student_id', 'course__code']
    search_fields = ['student__student_id', 'course__code', 'student__user__username']
    ordering_fields = ['enrollment_date', 'score', 'status']
    ordering = ['-enrollment_date']
    
    @action(detail=True, methods=['post'])
    def submit_grade(self, request, pk=None):
        """Submit or update grade for an enrollment"""
        enrollment = self.get_object()
        
        if 'score' in request.data:
            enrollment.score = request.data['score']
        
        if 'attendance_percentage' in request.data:
            enrollment.attendance_percentage = request.data['attendance_percentage']
        
        if 'notes' in request.data:
            enrollment.notes = request.data['notes']
        
        enrollment.save()
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete_enrollment(self, request, pk=None):
        """Mark an enrollment as completed"""
        enrollment = self.get_object()
        enrollment.status = 'COMPLETED'
        enrollment.completed_date = __import__('django.utils.timezone', fromlist=['now']).now().date()
        enrollment.save()
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data)
