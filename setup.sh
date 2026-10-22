#!/bin/bash

# Student Management System - Quick Setup Script
# For Build Bright University (BBU)

echo "🎓 ប្រព័ន្ធគ្រប់គ្រងនិស្សិត - ការរៀបចំលឿន"
echo "Student Management System - Quick Setup"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 ការបង្កើត Virtual Environment..."
    if command -v python3.12 &> /dev/null; then
        PYTHON_CMD=python3.12
    else
        PYTHON_CMD=python3
    fi
    $PYTHON_CMD -m venv venv
    echo "✅ Virtual Environment បង្កើតចប់ ($PYTHON_CMD)"
else
    echo "✅ Virtual Environment មាន"
fi

echo ""
echo "🔄 ចាប់ផ្តើម Virtual Environment..."
source venv/bin/activate

echo ""
echo "📥 ដំឡើង Dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies ដំឡើងចប់"

echo ""
echo "🗄️ ដាក់ដំណើរការ Migrations..."
python manage.py makemigrations -q
python manage.py migrate -q
echo "✅ Migrations ដាក់ដំណើរការចប់"

echo ""
echo "👨‍💼 បង្កើត Superuser (Admin)..."
echo "ឈ្មោះប្រើប្រាស់: admin"
echo "អ៊ីមែល: admin@example.com"
echo "ល៍ឈ្មោះសម្ងាត់: admin123456"

python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123456')
    print("✅ Superuser admin បង្កើតចប់")
else:
    print("⚠️ Superuser admin មាន")
END

echo ""
echo "✨ ការរៀបចំលឿនគ្រប់គ្រងចប់!"
echo ""
echo "📝 ដូចម្តេច ចាប់ផ្តើម:"
echo "1. ដាក់ដំណើរការ server: python manage.py runserver"
echo "2. ចូលក្នុង Admin: http://127.0.0.1:8000/admin/"
echo "3. ចូលក្នុង Home: http://127.0.0.1:8000/"
echo ""
echo "📚 ឯកសារលម្អិត (Lessons & Documentation):"
echo "- lessons/INSTRUCTIONS_KH.md (ឯកសារក្នុងខ្មែរ)"
echo "- lessons/PRACTICE_EXERCISES_KH.md (លំហាត់ 60+ ឧបាយកលបង្ហាប់)"
echo "- lessons/DOCUMENTATION_INDEX.md (មាតិកាឯកសារទាំងអស់)"
echo "- README.md (ឯកសារ English)"
echo ""
