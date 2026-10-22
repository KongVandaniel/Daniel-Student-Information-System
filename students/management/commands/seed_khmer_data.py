from django.core.management.base import BaseCommand
from scripts.generate_khmer_data import run_seed

class Command(BaseCommand):
    help = 'Randomly generates realistic Khmer students, IT courses, and enrollments'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1000,
            help='Number of student records to generate (default: 1000)',
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.NOTICE(f'Generating {count} student records with IT courses and enrollments...'))
        run_seed(count)
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} students with IT courses and enrollments!'))
