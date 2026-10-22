# 📚 ប្រព័ន្ធគ្រប់គ្រងនិស្សិត Django
## Student Management System - Full-Stack Project

### 🎓 ដោយ Build Bright University (BBU)

---

## 📋 ព័ត៌មាននៃគម្រោង (Project Description)

ប្រព័ន្ធគ្រប់គ្រងនិស្សិតនេះគឺជាគម្រោង Django ពេញលេញដែលផ្គាប់ដៀមលម្អិត សម្រាប់រៀនដូច្នេះ និងការបង្ហាញលក្ខណៈពិសេស។ គម្រោងនេះគ្របដណ្តប់វគ្គសិក្សាលម្អិតលម្អិត រចនាសម្ព័ន្ធដែលលម្អិត ហើយលម្អិតលម្អិត។

### 🎯 គោលបំណង (Objectives)

គម្រោងនេះគឺដើម្បី៖
- ✅ បង្ហាញស្ថាបត្យកម្ម MVT នៃ Django
- ✅ ផ្តល់ឧទាហរណ៍ពេញលេញនៃ CRUD operations
- ✅ បង្ហាញ Function-Based និង Class-Based Views
- ✅ សាកល្បង Django ORM និង Models
- ✅ បង្ហាញ Django Admin Panel
- ✅ បង្កើត REST APIs ដោយប្រើ Django REST Framework
- ✅ ផ្តល់ឧបាយកលបង្ហាប់សម្រាប់ 60+ practice problems

---

## 🚀 ការដំឡើង (Installation)

### ១. Clone Project

```bash
cd /path/to/django_lesson
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### ២. ដំឡើង Dependencies

```bash
pip install -r requirements.txt
```

### ៣. ដាក់ដំណើរការ Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### ៤. បង្កើត Superuser (Admin Account)

```bash
python manage.py createsuperuser
# បង្ហាញឈ្មោះប្រើប្រាស់, អ៊ីមែល, ល ស្ទាប់

# ឧទាហរណ៍:
# Username: admin
# Email: admin@example.com
# Password: admin123
```

### ៥. ដាក់ដំណើរការ Development Server

```bash
python manage.py runserver
```

ចូលប្រើប្រាស់នៅ `http://127.0.0.1:8000/`

### ៦. ចូលក្នុង Admin Panel

ចូលក្នុង `http://127.0.0.1:8000/admin/` ដោយប្រើ superuser credentials

---

## 📁 រចនាសម្ព័ន្ធគម្រោង (Project Structure)

```
django_lesson/
├── manage.py
├── requirements.txt
├── README.md                   # This file
├── lessons/                    # All Lesson Materials & Documentation
│   ├── INSTRUCTIONS_KH.md      # Comprehensive Guide in Khmer (6 Parts)
│   ├── STATIC_FILES_GUIDE_KH.md# Static Files Setup & Usage Guide (Khmer)
│   ├── MEDIA_FILES_GUIDE_KH.md # Media Files & Uploads Guide (Khmer)
│   ├── PRACTICE_EXERCISES_KH.md# 60 Practice Exercises with Solutions
│   ├── INSTRUCTOR_GUIDE.md     # Lesson Plans for Instructors
│   ├── QUICKSTART.md           # 5-min Quickstart
│   └── DOCUMENTATION_INDEX.md  # Master Documentation Index
├── scripts/                    # Utility & Seeding Scripts
│   └── generate_khmer_data.py  # Realistic Khmer Student Data Generator
├── server_logs/                # Application & Server Logs
│   └── server.log              # Server logs
│
├── student_system/             # Main Project
│   ├── settings.py            # Configuration
│   ├── urls.py                # Project URLs
│   ├── wsgi.py                # WSGI Configuration
│   ├── serializers.py         # DRF Serializers
│   ├── api_views.py           # API ViewSets
│   └── api_urls.py            # API URLs
│
├── students/                   # Student App
│   ├── models.py              # Student Model
│   ├── views.py               # FBV & CBV
│   ├── forms.py               # ModelForms
│   ├── admin.py               # Admin Configuration
│   ├── urls.py                # App URLs
│   └── migrations/            # Database Migrations
│
├── courses/                    # Course App
│   ├── models.py              # Course Model
│   ├── views.py               # Views
│   ├── forms.py               # Forms
│   ├── admin.py               # Admin
│   ├── urls.py                # URLs
│   └── migrations/
│
├── enrollments/                # Enrollment App
│   ├── models.py              # Enrollment Model
│   ├── views.py               # Views
│   ├── forms.py               # Forms
│   ├── admin.py               # Admin
│   ├── urls.py                # URLs
│   └── migrations/
│
├── templates/                  # HTML Templates
│   ├── base.html              # Base Template
│   ├── students/              # Student Templates
│   ├── courses/               # Course Templates
│   └── enrollments/           # Enrollment Templates
│
├── static/                     # Static Files
│   ├── css/
│   └── js/
│
├── media/                      # User Uploads
│   └── profiles/              # Student Profiles
│
└── venv/                       # Virtual Environment
```

---

## 🔑 ក្នុងគម្រោង (Key Features)

### 1️⃣ Models (ស្រទាប់ទិន្នន័យ)

- **Student**: ពត៌មាននិស្សិត (ឈ្មោះ, ID, GPA, ចាប់ផ្តើមលើម, ល)
- **Course**: ពត៌មានវគ្គ (ឈ្មោះ, សម្ងាត់, កម្រិត, សមត្ថភាព, ល)
- **Enrollment**: ការចុះឈ្មោះសិស្សក្នុងវគ្គ (ពិន្ទុ, ថ្នាក់, ស្ថានភាព, ល)

### 2️⃣ Views (ឡូកិក)

- **Function-Based Views (FBV)**: សម្រាប់ logic ងាយ
- **Class-Based Views (CBV)**: សម្រាប់ logic ស្មុគស្មាញ និង reusability

### 3️⃣ URLs & Routing

- ដាច់ដោយឡែក URL patterns សម្រាប់ app នីមួយៗ
- Dynamic URL parameters (e.g., `<int:pk>`, `<str:username>`)

### 4️⃣ Templates

- Base template inheritance
- Template tags និង filters
- Form rendering

### 5️⃣ Forms

- ModelForms សម្រាប់ CRUD operations
- Custom form validation
- CSRF protection

### 6️⃣ Admin Panel

- Register models ក្នុង Django Admin
- Custom list_display, filters, search
- Custom admin actions

### 7️⃣ Authentication

- Login/Logout system
- Permission-based access control
- @login_required decorators

### 8️⃣ REST API

- Django REST Framework ViewSets
- Serializers សម្រាប់ JSON conversion
- Token Authentication
- Pagination, Filtering, Searching

---

## 🛣️ API Endpoints

```
GET     /api/students/              - List all students
POST    /api/students/              - Create new student
GET     /api/students/{id}/         - Get student details
PUT     /api/students/{id}/         - Update student
DELETE  /api/students/{id}/         - Delete student
GET     /api/students/{id}/enrollments/ - Get student enrollments
GET     /api/students/{id}/transcript/   - Get student transcript

GET     /api/courses/               - List all courses
POST    /api/courses/               - Create new course
GET     /api/courses/{id}/          - Get course details
PUT     /api/courses/{id}/          - Update course
DELETE  /api/courses/{id}/          - Delete course
GET     /api/courses/{id}/students/ - Get enrolled students
GET     /api/courses/{id}/enrollment_statistics/ - Get stats

GET     /api/enrollments/           - List all enrollments
POST    /api/enrollments/           - Create enrollment
GET     /api/enrollments/{id}/      - Get enrollment details
PUT     /api/enrollments/{id}/      - Update enrollment
DELETE  /api/enrollments/{id}/      - Delete enrollment
POST    /api/enrollments/{id}/submit_grade/ - Submit grades
POST    /api/enrollments/{id}/complete_enrollment/ - Mark complete
```

---

## 📖 ឯកសារ (Documentation)

### ចូលក្នុង Khmer Language ឯកសារ (ក្នុងថត lessons/)

1. **[lessons/INSTRUCTIONS_KH.md](lessons/INSTRUCTIONS_KH.md)** - Complete guide in Khmer covering:
   - ផ្នែកទី១-៦: ការរៀនលម្អិត
   - Code examples
   - ពន្យល់ទូលំទូលាយ

2. **[lessons/STATIC_FILES_GUIDE_KH.md](lessons/STATIC_FILES_GUIDE_KH.md)** - Static Files Complete Guide:
   - ការរៀបចំ CSS, JS, Images, និង Fonts
   - ការកំណត់ `STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT`
   - Production deployment ជាមួយ `collectstatic` និង WhiteNoise

3. **[lessons/MEDIA_FILES_GUIDE_KH.md](lessons/MEDIA_FILES_GUIDE_KH.md)** - Media Files & Uploads Complete Guide:
   - ការរៀបចំ Pillow, `ImageField`, និង `FileField`
   - ការកំណត់ `MEDIA_URL`, `MEDIA_ROOT`
   - ការប្រើប្រាស់ `enctype="multipart/form-data"` និង `request.FILES`
   - ការបង្ហាញរូបភាពក្នុង Templates និង Cloud Storage (AWS S3)

4. **[lessons/GIT_AND_DEPLOYMENT_GUIDE_KH.md](lessons/GIT_AND_DEPLOYMENT_GUIDE_KH.md)** - Git & Cloud Deployment Complete Guide:
   - ការគ្រប់គ្រង `.gitignore` និងសុវត្ថិភាព `.env`
   - ជំហាន Push កូដទៅកាន់ GitHub
   - ការដាក់ឱ្យដំណើរការលើ Render (Blueprint `render.yaml` & Manual Web Service)
   - ការដាក់ឱ្យដំណើរការលើ Heroku (Heroku CLI, Postgres Add-on, `Procfile`)
   - ស្ថាបត្យកម្ម Production: Gunicorn + WhiteNoise + PostgreSQL
   - ការដោះស្រាយកំហុស Deployment (CSRF, Allowed Hosts, Static files)

5. **[lessons/INDIVIDUAL_ASSIGNMENT_GUIDE_KH.md](lessons/INDIVIDUAL_ASSIGNMENT_GUIDE_KH.md)** - Individual Assignment Guide (ថ្នាក់ A1IT-B103):
   - មគ្គុទ្ទេសក៍កិច្ចការបុគ្គល៖ Theme Adaptation & Cloud Deployment
   - ការកែសម្រួល UI/Theme/Branding ដោយរក្សារចនាសម្ព័ន្ធ Core Software
   - ការ Push ឡើង GitHub និង Deploy លើ Render
   - របៀបដាក់កិច្ចការលើ Platform [https://bbusrithub.site/](https://bbusrithub.site/)
   - តារាងពិន្ទុ និងលក្ខខណ្ឌវាយតម្លៃ (Grading Rubric - 100 ពិន្ទុ)

6. **[lessons/PRACTICE_EXERCISES_KH.md](lessons/PRACTICE_EXERCISES_KH.md)** - 60 practical problems:
   - ១០ ឧបាយកលបង្ហាប់ក្នុងផ្នែក
   - Solutions និង explanations
   - Progressively challenging

7. **[scripts/generate_khmer_data.py](scripts/generate_khmer_data.py)** - Data Seeding:
   - Generate realistic Khmer student profiles, IT courses, and enrollments
   - Command: `python manage.py seed_khmer_data --count 1000`

---

## 🏃 ដំណើរការ (Quick Start)

### ១. ចាប់ផ្តើម Server

```bash
python manage.py runserver
```

### ២. ចូលក្នុង Admin Panel

- URL: `http://127.0.0.1:8000/admin/`
- Username: `admin`
- Password: (លេខសម្ងាត់ដែលបង្កើតរបស់អ្នក)

### ៣. ចូលក្នុង Websites

- Students: `http://127.0.0.1:8000/students/`
- Courses: `http://127.0.0.1:8000/courses/`
- Enrollments: `http://127.0.0.1:8000/enrollments/`

### ៤. ចូលក្នុង API

- API Root: `http://127.0.0.1:8000/api/`
- Students API: `http://127.0.0.1:8000/api/students/`
- Courses API: `http://127.0.0.1:8000/api/courses/`
- Enrollments API: `http://127.0.0.1:8000/api/enrollments/`

---

## 🔧 Command-Line

```bash
# Create sample data
python manage.py shell
>>> from students.models import Student
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('student1', 'student1@example.com', 'password123')
>>> student = Student.objects.create(
...     user=user,
...     student_id='S001',
...     date_of_birth='2000-01-15',
...     gender='M',
...     city='Phnom Penh',
...     country='Cambodia'
... )
>>> exit()

# Run tests
python manage.py test

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Shell access
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic --noinput

# Check deployment readiness
python manage.py check --deploy
```

---

## 🚀 Deployment Guide

### Option 1: Render.com (Recommended)

1. Create `render.yaml` file
2. Connect GitHub repository
3. Deploy from dashboard

### Option 2: Heroku

```bash
heroku login
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Option 3: DigitalOcean/AWS

- Set up Ubuntu server
- Install Python, PostgreSQL
- Configure Gunicorn + Nginx
- Set up SSL certificate

---

## 📚 Learning Path

Follow this order for comprehensive learning:

1. **Week 1**: ចាប់ផ្តើម Architecture & Models (INSTRUCTIONS_KH.md Part 1-2)
2. **Week 2**: Views & URL Routing (Part 3) + Practice 1-20
3. **Week 3**: Templates & Forms (Part 4) + Practice 21-40
4. **Week 4**: Admin & Authentication (Part 5) + Practice 41-50
5. **Week 5**: REST API & Deployment (Part 6) + Practice 51-60

---

## 💻 System Requirements

- Python 3.9+
- Django 4.2
- pip (Python package manager)
- 2GB RAM minimum
- macOS, Linux, or Windows

---

## 📝 ឯកសារលម្អិត (Lessons & Documentation Reference)

| ឯកសារ (File) | ការពិពណ៌នា (Description) |
|-------------|-------------------------|
| [lessons/INSTRUCTIONS_KH.md](lessons/INSTRUCTIONS_KH.md) | 12-part comprehensive guide in Khmer (មគ្គុទ្ទេសក៍ពេញលេញ) |
| [lessons/STATIC_FILES_GUIDE_KH.md](lessons/STATIC_FILES_GUIDE_KH.md) | Complete guide on Static Files setup & usage (មគ្គុទ្ទេសក៍ Static Files) |
| [lessons/MEDIA_FILES_GUIDE_KH.md](lessons/MEDIA_FILES_GUIDE_KH.md) | Complete guide on Media Files & Uploads (មគ្គុទ្ទេសក៍ Media Files) |
| [lessons/GIT_AND_DEPLOYMENT_GUIDE_KH.md](lessons/GIT_AND_DEPLOYMENT_GUIDE_KH.md) | Git, GitHub & Cloud Deployment Guide (Render & Heroku) |
| [lessons/INDIVIDUAL_ASSIGNMENT_GUIDE_KH.md](lessons/INDIVIDUAL_ASSIGNMENT_GUIDE_KH.md) | Individual Assignment Guide (Theme Customization & Render Deployment) |
| [lessons/PRACTICE_EXERCISES_KH.md](lessons/PRACTICE_EXERCISES_KH.md) | 60+ exercises with solutions (លំហាត់អនុវត្តន៍ និងចម្លើយ) |
| [lessons/INSTRUCTOR_GUIDE.md](lessons/INSTRUCTOR_GUIDE.md) | Teaching methodology and lesson plans for instructors |
| [lessons/QUICKSTART.md](lessons/QUICKSTART.md) | 5-minute quickstart guide |
| [lessons/DOCUMENTATION_INDEX.md](lessons/DOCUMENTATION_INDEX.md) | Master index for all lessons, action plans, and audit reports |
| [README.md](README.md) | Project overview and setup instructions |
| `requirements.txt` | Python dependencies |
| `manage.py` | Django management tool |

---

## 🎓 ដូចម្តេចដើម្បីរៀន (How to Learn)

ប្រើប្រាស់ធនធានរបស់ Build Bright University (BBU)៖

1. Follow [lessons/INSTRUCTIONS_KH.md](lessons/INSTRUCTIONS_KH.md) step-by-step
2. Complete all 60+ practice exercises in [lessons/PRACTICE_EXERCISES_KH.md](lessons/PRACTICE_EXERCISES_KH.md)
3. Modify code and observe changes in the running application
4. Consult instructor guide in [lessons/INSTRUCTOR_GUIDE.md](lessons/INSTRUCTOR_GUIDE.md)
5. Explore the master index in [lessons/DOCUMENTATION_INDEX.md](lessons/DOCUMENTATION_INDEX.md)

---

## 📞 Support & Questions

For questions or issues:
1. Check [lessons/INSTRUCTIONS_KH.md](lessons/INSTRUCTIONS_KH.md)
2. Review [lessons/PRACTICE_EXERCISES_KH.md](lessons/PRACTICE_EXERCISES_KH.md)
3. Consult Django documentation: https://docs.djangoproject.com/
4. Ask instructor during office hours

---

## 📜 License

This project is created for educational purposes at Build Bright University.

---

## 👨‍🏫 ដើម្បីគ្រូ (For Instructors)

This is a complete demo project ready for classroom use:
- ✅ Live demonstrations
- ✅ Code walkthroughs
- ✅ Student assignments
- ✅ Practical exercises
- ✅ API testing
- ✅ Admin panel management

---

### 🌟 Happy Learning! សប្ដាធម្ម!

