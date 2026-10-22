"""
Application entry-point alias for Cloud platforms (such as Render)
that default to `gunicorn app:app` or `app.py`.
"""
import sys
from django.core.management import call_command
from student_system.wsgi import application

# Automatically run database migrations and setup test data on server startup
# Ensures tables and admin user (admin / admin123456) always exist
try:
    call_command('migrate', interactive=False)
    call_command('setup_test_data', student_count=100, interactive=False)
except Exception as e:
    print(f"Startup setup notice: {e}", file=sys.stderr)

# Expose WSGI application callable as `app`
app = application
