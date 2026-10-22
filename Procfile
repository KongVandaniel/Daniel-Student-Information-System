web: python manage.py migrate && python manage.py setup_test_data --student-count 100 && gunicorn student_system.wsgi:application --log-file -
release: python manage.py migrate && python manage.py setup_test_data --student-count 100
