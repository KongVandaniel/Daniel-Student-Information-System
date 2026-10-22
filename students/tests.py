from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from students.models import Student
from datetime import date

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='testpassword123'
        )
        self.student = Student.objects.create(
            user=self.user,
            student_id='STU101',
            date_of_birth=date(2001, 5, 20),
            gender='M',
            phone_number='012345678',
            address='Street 271',
            city='Phnom Penh',
            country='Cambodia'
        )

    def test_student_str(self):
        self.assertEqual(str(self.student), 'STU101 - John Doe')

    def test_student_str_with_khmer_name_as_primary(self):
        self.student.khmer_name = 'សុខ តារា'
        self.student.save()
        self.assertEqual(str(self.student), 'STU101 - សុខ តារា')
        self.assertEqual(self.student.get_primary_name(), 'សុខ តារា')

    def test_student_absolute_url(self):
        self.assertEqual(
            self.student.get_absolute_url(),
            reverse('students:student_detail', kwargs={'pk': self.student.pk})
        )


class StudentViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='teacher',
            password='password123'
        )
        self.student = Student.objects.create(
            user=self.user,
            student_id='STU202',
            date_of_birth=date(2002, 1, 1),
            gender='F',
            address='Street 10',
            city='Siem Reap',
            country='Cambodia'
        )

    def test_student_list_login_required(self):
        response = self.client.get(reverse('students:student_list'))
        self.assertEqual(response.status_code, 302)

    def test_student_list_authenticated(self):
        self.client.login(username='teacher', password='password123')
        self.student.khmer_name = 'ជា ពិសិដ្ឋ'
        self.student.save()
        response = self.client.get(reverse('students:student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'STU202')
        self.assertContains(response, 'ជា ពិសិដ្ឋ')
        # Check avatar and two name columns presence
        self.assertContains(response, 'Photo')
        self.assertContains(response, 'Khmer Name')
        self.assertContains(response, 'English Name')

    def test_student_list_search_by_khmer_name(self):
        self.client.login(username='teacher', password='password123')
        self.student.khmer_name = 'ហេង មុនី'
        self.student.save()
        response = self.client.get(reverse('students:student_list') + '?q=មុនី')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ហេង មុនី')
        self.assertContains(response, 'STU202')

    def test_student_register_page(self):
        response = self.client.get(reverse('students:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Khmer Name')

    def test_student_detail_view(self):
        self.client.login(username='teacher', password='password123')
        self.student.khmer_name = 'កែវ សម្បត្តិ'
        self.student.save()
        response = self.client.get(reverse('students:student_detail', kwargs={'pk': self.student.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'STU202')
        self.assertContains(response, 'កែវ សម្បត្តិ')
        self.assertContains(response, '<strong>English Name:</strong>')
        self.assertContains(response, '<strong>Enrollment Date:</strong>')
        # Ensure no raw unparsed template tags are rendered in HTML
        self.assertNotContains(response, '{{')

    def test_student_cbv_create_and_update(self):
        self.client.login(username='teacher', password='password123')
        # Test CBV create
        response = self.client.post(reverse('students:student_create_cbv'), {
            'student_id': 'STU999',
            'khmer_name': 'សុខ វិបុល',
            'date_of_birth': '2002-04-15',
            'gender': 'M',
            'phone_number': '012999888',
            'address': 'St 123',
            'city': 'Phnom Penh',
            'country': 'Cambodia',
        })
        self.assertEqual(response.status_code, 302)
        created = Student.objects.filter(student_id='STU999').first()
        self.assertIsNotNone(created)
        self.assertEqual(created.khmer_name, 'សុខ វិបុល')

        # Test CBV update
        response_update = self.client.post(reverse('students:student_update_cbv', kwargs={'pk': created.pk}), {
            'student_id': 'STU999',
            'khmer_name': 'សុខ វិបុល រតនៈ',
            'date_of_birth': '2002-04-15',
            'gender': 'M',
            'phone_number': '012999888',
            'address': 'St 123',
            'city': 'Phnom Penh',
            'country': 'Cambodia',
        })
        self.assertEqual(response_update.status_code, 302)
        created.refresh_from_db()
        self.assertEqual(created.khmer_name, 'សុខ វិបុល រតនៈ')


class RootEndpointsTest(TestCase):
    def test_favicon_redirect(self):
        response = self.client.get('/favicon.ico')
        self.assertEqual(response.status_code, 301)
        self.assertIn('favicon.ico', response.get('Location'))

    def test_chrome_devtools_probe(self):
        response = self.client.get('/.well-known/appspecific/com.chrome.devtools.json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})


class SetupTestDataCommandTest(TestCase):
    def test_setup_test_data_creates_admin_and_data(self):
        from io import StringIO
        from django.core.management import call_command
        from django.contrib.auth import authenticate

        out = StringIO()
        call_command('setup_test_data', student_count=5, stdout=out)
        user = authenticate(username='admin', password='admin123456')
        self.assertIsNotNone(user)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertGreaterEqual(Student.objects.count(), 5)


