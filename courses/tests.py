# student_system/courses/tests.py

# import TestCase and Client from django.test module for testing
from django.test import TestCase, Client
# import reverse from django.urls module for URL reversal
from django.urls import reverse
# import User from django.contrib.auth.models module for user authentication and authorization
from django.contrib.auth.models import User
# import Course model from courses.models module for testing
from courses.models import Course
# import date from datetime module for date operations
from datetime import date

# define CourseModelTest class to test the course model
class CourseModelTest(TestCase):
    # setUp method is used to set up the test environment
    # it is used to create a course for testing
    def setUp(self):
        # create an instructor user for testing
        self.instructor = User.objects.create_user(username='prof_smith', password='password123')
        # create a course for testing
        self.course = Course.objects.create(
            code='CS201',
            title='Data Structures',
            description='Study algorithms and data structures',
            instructor=self.instructor,
            credits=3,
            level='200',
            capacity=40,
            status='ACTIVE',
            start_date=date(2024, 1, 15),
            end_date=date(2024, 6, 15),
        )

    # test_course_str method is used to test the string representation of the model
    # it is used to check if the string representation of the model is correct
    def test_course_str(self):
        self.assertEqual(str(self.course), 'CS201 - Data Structures')

    # test_course_is_available method is used to test the is_available property of the model
    # it is used to check if the is_available property of the model is correct
    def test_course_is_available(self):
        self.assertTrue(self.course.is_available)
        self.course.status = 'INACTIVE'
        self.assertFalse(self.course.is_available)

    # test_course_absolute_url method is used to test the absolute URL of the model
    # it is used to check if the absolute URL of the model is correct
    def test_course_absolute_url(self):
        self.assertEqual(
            self.course.get_absolute_url(),
            reverse('courses:course_detail', kwargs={'pk': self.course.pk})
        )

# define CourseViewsTest class to test the course views
class CourseViewsTest(TestCase):
    # setUp method is used to set up the test environment
    # it is used to create a course for testing
    def setUp(self):
        # create a client for testing
        self.client = Client()
        # create a user for testing
        self.user = User.objects.create_user(username='teacher', password='password123')
        # create a course for testing
        self.course = Course.objects.create(
            code='CS301',
            title='Web Development',
            description='Django and React',
            instructor=self.user,
            credits=3,
            level='300',
            capacity=30,
            status='ACTIVE',
            start_date=date(2024, 2, 1),
            end_date=date(2024, 7, 1),
        )

    # test_course_list_view method is used to test the course list view
    # it is used to check if the course list view is correct
    def test_course_list_view(self):
        response = self.client.get(reverse('courses:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CS301')

    # test_course_detail_view method is used to test the course detail view
    # it is used to check if the course detail view is correct
    def test_course_detail_view(self):
        response = self.client.get(reverse('courses:course_detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Development')

    # test_course_create_requires_login method is used to test the course create view
    # it is used to check if the course create view is correct
    def test_course_create_requires_login(self):
        response = self.client.get(reverse('courses:course_create')) #
        self.assertEqual(response.status_code, 302)

    # test_course_create_authenticated method is used to test the course create view
    # it is used to check if the course create view is correct
        self.client.login(username='teacher', password='password123')
        response = self.client.get(reverse('courses:course_create'))
        self.assertEqual(response.status_code, 200)
