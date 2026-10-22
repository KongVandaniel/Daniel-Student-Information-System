from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment

class SystemAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testadmin', password='Password@123', is_staff=True)
        self.client.force_authenticate(user=self.user)

        self.student_user = User.objects.create_user(
            username='student1', first_name='Sokha', last_name='Chan', email='sokha@bbu.edu.kh'
        )
        self.student = Student.objects.create(
            user=self.student_user,
            student_id='BBU2026001',
            khmer_name='ចាន់ សុខា',
            date_of_birth=date(2003, 5, 12),
            gender='M',
            phone_number='012345678',
            address='Street 271, Sangkat Boeung Tumpun',
            city='Phnom Penh',
            country='Cambodia',
            gpa=3.75,
            is_active=True
        )

        self.instructor = User.objects.create_user(username='instructor1', first_name='Dr. Keo', last_name='Sok')
        self.course = Course.objects.create(
            code='IT-101',
            title='Introduction to Information Technology',
            description='Fundamentals of hardware, software, and networking.',
            instructor=self.instructor,
            credits=3,
            level='100',
            capacity=35,
            status='ACTIVE',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 5, 30)
        )

        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            status='COMPLETED',
            score=92.50,
            attendance_percentage=95.00
        )

    def test_home_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_api_list(self):
        response = self.client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        self.assertGreaterEqual(len(results), 1)

    def test_student_api_detail(self):
        response = self.client.get(f'/api/students/{self.student.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_id'], 'BBU2026001')
        self.assertEqual(response.data['khmer_name'], 'ចាន់ សុខា')

    def test_student_api_search_khmer_name(self):
        response = self.client.get('/api/students/?search=សុខា')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['student_id'], 'BBU2026001')

    def test_student_api_enrollments_action(self):
        response = self.client.get(f'/api/students/{self.student.pk}/enrollments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_api_transcript_action(self):
        response = self.client.get(f'/api/students/{self.student.pk}/transcript/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_id'], 'BBU2026001')
        self.assertEqual(response.data['completed_courses'], 1)
        self.assertAlmostEqual(response.data['average_score'], 92.5)

    def test_course_api_list_and_detail(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_detail = self.client.get(f'/api/courses/{self.course.pk}/')
        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(response_detail.data['code'], 'IT-101')

    def test_course_api_students_and_stats(self):
        students_resp = self.client.get(f'/api/courses/{self.course.pk}/students/')
        self.assertEqual(students_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(students_resp.data), 1)

        stats_resp = self.client.get(f'/api/courses/{self.course.pk}/enrollment_statistics/')
        self.assertEqual(stats_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(stats_resp.data['total_completed'], 1)

    def test_enrollment_api_submit_grade(self):
        course2 = Course.objects.create(
            code='IT-102',
            title='Web Development with Django',
            description='Web fundamentals and backend architecture.',
            instructor=self.instructor,
            credits=3,
            level='200',
            capacity=30,
            status='ACTIVE',
            start_date=date(2026, 2, 1),
            end_date=date(2026, 6, 30)
        )
        new_enrollment = Enrollment.objects.create(
            student=self.student,
            course=course2,
            status='ENROLLED'
        )
        response = self.client.post(
            f'/api/enrollments/{new_enrollment.pk}/submit_grade/',
            {'score': 88.0, 'attendance_percentage': 90.0},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_enrollment.refresh_from_db()
        self.assertEqual(new_enrollment.grade, 'B')
        self.assertEqual(float(new_enrollment.score), 88.0)
