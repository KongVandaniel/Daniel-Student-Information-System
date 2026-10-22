from rest_framework import serializers
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True, required=False
    )
    
    class Meta:
        model = Student
        fields = ['id', 'user', 'user_id', 'student_id', 'khmer_name', 'date_of_birth', 'gender', 
                  'phone_number', 'address', 'city', 'country', 'profile_picture', 'gpa', 
                  'is_active', 'enrollment_date']
        read_only_fields = ['enrollment_date']

class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model"""
    instructor = UserSerializer(read_only=True)
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='instructor', write_only=True, required=False, allow_null=True
    )
    enrollment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'code', 'title', 'description', 'instructor', 'instructor_id',
                  'credits', 'level', 'capacity', 'status', 'start_date', 
                  'end_date', 'enrollment_count']
    
    def get_enrollment_count(self, obj):
        return obj.enrollments.count()

class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model"""
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source='student', write_only=True
    )
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'student_id', 'course_id', 'status', 'grade', 'score', 
                  'attendance_percentage', 'notes', 'enrollment_date', 'completed_date']
        read_only_fields = ['enrollment_date']

class EnrollmentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Enrollment including student and course info"""
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student_id', 'course_code', 'course_title', 'status', 
                  'grade', 'score', 'attendance_percentage', 'notes', 
                  'enrollment_date', 'completed_date']
