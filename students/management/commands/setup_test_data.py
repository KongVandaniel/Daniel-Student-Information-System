"""
Django Management Command: setup_test_data
Build Bright University (BBU) - Student Management System

Sets up initial deployment state:
1. Creates or updates admin superuser (admin / admin123456)
2. Automatically generates dummy test data (Khmer students, IT courses, enrollments) if DB is empty
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment


class Command(BaseCommand):
    help = 'Prepares database for deployment by creating admin superuser and populating test data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-user',
            type=str,
            default='admin',
            help='Superuser username (default: admin)',
        )
        parser.add_argument(
            '--admin-pass',
            type=str,
            default='admin123456',
            help='Superuser password (default: admin123456)',
        )
        parser.add_argument(
            '--admin-email',
            type=str,
            default='admin@bbu.edu.kh',
            help='Superuser email (default: admin@bbu.edu.kh)',
        )
        parser.add_argument(
            '--student-count',
            type=int,
            default=100,
            help='Number of test students to seed if database is empty (default: 100)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-seeding test data even if students already exist',
        )
        parser.add_argument(
            '--no-input', '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help='Do NOT prompt the user for input of any kind.',
        )

    def handle(self, *args, **options):
        admin_username = options['admin_user']
        admin_password = options['admin_pass']
        admin_email = options['admin_email']
        student_count = options['student_count']
        force = options['force']

        self.stdout.write(self.style.MIGRATE_HEADING("⚙️  Running Deployment Data Initialization..."))

        # 1. Create or update superuser
        user, created = User.objects.get_or_create(username=admin_username)
        user.email = admin_email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(admin_password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"  👤 Created superuser '{admin_username}' with password '{admin_password}'"))
        else:
            self.stdout.write(self.style.SUCCESS(f"  👤 Updated existing superuser '{admin_username}' with password '{admin_password}'"))

        # 2. Check and seed test data
        existing_students = Student.objects.count()
        existing_courses = Course.objects.count()

        if existing_students == 0 or force:
            self.stdout.write(self.style.NOTICE(f"  🌱 Populating test data ({student_count} Khmer students, IT courses, enrollments)..."))
            try:
                from scripts.generate_khmer_data import run_seed
                run_seed(student_count)
                self.stdout.write(self.style.SUCCESS(f"  ✅ Test data created: {Student.objects.count()} students, {Course.objects.count()} courses, {Enrollment.objects.count()} enrollments."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ Error seeding test data: {e}"))
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"  ℹ️ Database already contains {existing_students} students and {existing_courses} courses. Skipping seeding (pass --force to re-seed)."
                )
            )

        self.stdout.write(self.style.SUCCESS("✨ Deployment data setup completed successfully!"))
