#!/usr/bin/env python
"""
Build Bright University (BBU) - Khmer Data Generator
Generates realistic Cambodian student profiles, IT courses, and course enrollments.
Target: 1,000+ students, 25 IT courses, 3,000+ enrollments.
"""

import os
import sys
import random
from datetime import date, timedelta
from decimal import Decimal

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
import django
django.setup()

from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment

# ==========================================
# Authentic Khmer Names & Data Dictionaries
# ==========================================

KHMER_LAST_NAMES = [
    ("Sok", "សុខ"), ("Chan", "ចាន់"), ("Chea", "ជា"), ("Heng", "ហេង"),
    ("Kim", "គីម"), ("Lim", "លីម"), ("Meng", "ម៉េង"), ("Pich", "ពេជ្រ"),
    ("Seng", "សេង"), ("Tep", "ទេព"), ("Vorn", "វ៉ន"), ("Yim", "យីម"),
    ("Ros", "រស់"), ("Keo", "កែវ"), ("Chhorn", "ឈន"), ("Ouk", "អ៊ុក"),
    ("Prak", "ប្រាក់"), ("San", "សាន"), ("Meas", "មាស"), ("Nget", "ង៉ែត"),
    ("Som", "សោម"), ("Duong", "ដួង"), ("Kong", "គង់"), ("Long", "ឡុង"),
    ("Sarun", "សារុន"), ("Khun", "ឃុន"), ("Bun", "ប៊ុន"), ("Ly", "លី"),
    ("Huy", "ហ៊ុយ"), ("Sin", "ស៊ីន"), ("Rath", "រ័ត្ន"), ("Phan", "ផាន់"),
    ("Sam", "សំ"), ("Touch", "ទូច"), ("Srun", "ស្រ៊ុន"), ("Em", "អ៊ឹម"),
    ("Roeun", "រឿន"), ("Chhum", "ឈុំ"), ("Nov", "ណុវ"), ("Pao", "ប៉ោ"),
    ("Hun", "ហ៊ុន"), ("Chhay", "ឆាយ"), ("Mao", "ម៉ៅ"), ("Khem", "ខែម"),
    ("Krouch", "ក្រូច"), ("Chrun", "ជ្រុន"), ("Taing", "តាំង"), ("Soeun", "សឿន")
]

KHMER_MALE_FIRST_NAMES = [
    ("Dara", "តារា"), ("Vichea", "វិជ្ជា"), ("Rithy", "រិទ្ធី"), ("Serey", "សិរី"),
    ("Kosal", "កុសល"), ("Vibol", "វិបុល"), ("Bunthoeun", "ប៊ុនធឿន"), ("Sovann", "សុវណ្ណ"),
    ("Chamroeun", "ចំរើន"), ("Makara", "មករា"), ("Piseth", "ពិសិដ្ឋ"), ("Sambath", "សម្បត្តិ"),
    ("Thavrak", "ថាវរ៉ាក់"), ("Veasna", "វាសនា"), ("Visal", "វិសាល"), ("Pharith", "ផារិទ្ធ"),
    ("Bora", "បូរ៉ា"), ("Khemara", "ខេមរា"), ("Rattanak", "រតនៈ"), ("Samnang", "សំណាង"),
    ("Sophea", "សុភា"), ("Seyha", "សីហា"), ("Oudom", "ឧត្តម"), ("Panha", "បញ្ញា"),
    ("Phearith", "ភារិទ្ធ"), ("Moni", "មុនី"), ("Vichet", "វិចិត្រ"), ("Reaksmey", "រស្មី"),
    ("Seyla", "សិលា"), ("Channarith", "ច័ន្ទណារិទ្ធ"), ("Davit", "ដាវីត"), ("Rathana", "រតនា"),
    ("Virak", "វីរៈ"), ("Sovanreach", "សុវណ្ណរាជ"), ("Roth", "រ័ត្ន"), ("Vireak", "វីរៈ")
]

KHMER_FEMALE_FIRST_NAMES = [
    ("Bopha", "បុប្ផា"), ("Channary", "ច័ន្ទណារី"), ("Dany", "ដានី"), ("Kolab", "កុលាប"),
    ("Malis", "ម្លិះ"), ("Phalla", "ផល្លា"), ("Rachana", "រចនា"), ("Sreymom", "ស្រីមុំ"),
    ("Thida", "ធីតា"), ("Vanny", "វ៉ាន់នី"), ("Neary", "នារី"), ("Kanha", "កញ្ញា"),
    ("Sreypov", "ស្រីពៅ"), ("Leakhena", "លក្ខិណា"), ("Chanlina", "ច័ន្ទលីណា"), ("Sophorn", "សោភ័ណ"),
    ("Chenda", "ចិន្តា"), ("Kunthea", "គន្ធា"), ("Monika", "ម៉ូនីកា"), ("Sotheavy", "សុធាវី"),
    ("Bophary", "បុប្ផារី"), ("Chanthou", "ច័ន្ទធូ"), ("Devi", "ទេវី"), ("Kalyan", "កល្យាណ"),
    ("Nita", "នីតា"), ("Sreynich", "ស្រីនិច"), ("Theary", "ធារី"), ("Voleak", "វល័ក្ខ"),
    ("Pisey", "ពិសី"), ("Sreyneat", "ស្រីនាត"), ("Chanthy", "ច័ន្ទធី"), ("Romdoul", "រំដួល")
]

CAMBODIAN_CITIES = [
    ("Phnom Penh", "រាជធានីភ្នំពេញ"),
    ("Siem Reap", "ខេត្តសៀមរាប"),
    ("Battambang", "ខេត្តបាត់ដំបង"),
    ("Kandal", "ខេត្តកណ្តាល"),
    ("Kampong Cham", "ខេត្តកំពង់ចាម"),
    ("Kampot", "ខេត្តកំពត"),
    ("Preah Sihanouk", "ខេត្តព្រះសីហនុ"),
    ("Takeo", "ខេត្តតាកែវ"),
    ("Prey Veng", "ខេត្តព្រៃវែង"),
    ("Kampong Thom", "ខេត្តកំពង់ធំ"),
    ("Kampong Speu", "ខេត្តកំពង់ស្ពឺ"),
    ("Pursat", "ខេត្តពោធិ៍សាត់"),
    ("Svay Rieng", "ខេត្តស្វាយរៀង"),
    ("Banteay Meanchey", "ខេត្តបន្ទាយមានជ័យ"),
    ("Kratie", "ខេត្តក្រចេះ")
]

KHMER_STREET_ADDRESSES = [
    "Sangkat Boeung Keng Kang 1, Khan Chamkarmon",
    "Sangkat Teuk Laak 1, Khan Toul Kork",
    "Sangkat Phsar Thmei 3, Khan Daun Penh",
    "Sangkat Kakab 1, Khan Por Sen Chey",
    "Sangkat Chroy Changvar, Khan Chroy Changvar",
    "Sangkat Toul Svay Prey 1, Khan Boeng Keng Kang",
    "Sangkat Phnom Penh Thmei, Khan Sen Sok",
    "Sangkat Svay Dangkum, Krong Siem Reap",
    "Sangkat Sala Kamreuk, Krong Siem Reap",
    "Sangkat Svay Por, Krong Battambang",
    "Sangkat Ratanak, Krong Battambang",
    "Sangkat Veal Vong, Krong Kampong Cham",
    "Sangkat Kampong Kandal, Krong Kampot",
    "Sangkat 4, Krong Preah Sihanouk",
    "Sangkat Roka Khnong, Krong Doun Kaev",
    "Sangkat Svay Rieng, Krong Svay Rieng"
]

PHONE_PREFIXES = [
    "010", "012", "015", "016", "017", "069", "070", "077", "078",
    "081", "086", "087", "089", "092", "093", "095", "096", "098", "099"
]

INSTRUCTORS_DATA = [
    ("dr_sok_piseth", "Piseth", "Sok (បណ្ឌិត សុខ ពិសិដ្ឋ)", "piseth.sok@bbu.edu.kh"),
    ("prof_heng_vichea", "Vichea", "Heng (សាស្ត្រាចារ្យ ហេង វិជ្ជា)", "vichea.heng@bbu.edu.kh"),
    ("dr_keo_dara", "Dara", "Keo (បណ្ឌិត កែវ តារា)", "dara.keo@bbu.edu.kh"),
    ("prof_chan_thavrak", "Thavrak", "Chan (សាស្ត្រាចារ្យ ចាន់ ថាវរ៉ាក់)", "thavrak.chan@bbu.edu.kh"),
    ("dr_meas_kanha", "Kanha", "Meas (បណ្ឌិត មាស កញ្ញា)", "kanha.meas@bbu.edu.kh"),
    ("prof_lim_vibol", "Vibol", "Lim (សាស្ត្រាចារ្យ លីម វិបុល)", "vibol.lim@bbu.edu.kh"),
    ("dr_tep_sovann", "Sovann", "Tep (បណ្ឌិត ទេព សុវណ្ណ)", "sovann.tep@bbu.edu.kh"),
    ("prof_pich_rachana", "Rachana", "Pich (សាស្ត្រាចារ្យ ពេជ្រ រចនា)", "rachana.pich@bbu.edu.kh"),
]

IT_COURSES_DATA = [
    # 100-Level Foundation Courses
    {
        "code": "CS101",
        "title": "Introduction to Computer Science (សេចក្តីផ្តើមវិទ្យាសាស្ត្រកុំព្យូទ័រ)",
        "description": "Fundamental concepts of computing, binary systems, algorithms, problem-solving, and computer ethics for IT freshmen at Build Bright University.",
        "credits": 3,
        "level": "100",
        "capacity": 45,
    },
    {
        "code": "IT102",
        "title": "Fundamentals of Information Technology (មូលដ្ឋានគ្រឹះព័ត៌មានវិទ្យា)",
        "description": "Overview of IT infrastructure, operating systems, hardware components, productivity suites, and modern office automation.",
        "credits": 3,
        "level": "100",
        "capacity": 50,
    },
    {
        "code": "CS103",
        "title": "Programming in C/C++ (ការសរសេរកម្មវិធីជាមួយ C/C++)",
        "description": "Structured programming principles, data types, pointers, memory allocation, control structures, and object-oriented foundations in C++.",
        "credits": 3,
        "level": "100",
        "capacity": 40,
    },
    {
        "code": "CS104",
        "title": "Computer Hardware & Architecture (ស្ថាបត្យកម្មនិងផ្នែករឹងកុំព្យូទ័រ)",
        "description": "CPU architecture, motherboard components, cache hierarchy, logic gates, peripheral buses, and PC assembly lab.",
        "credits": 3,
        "level": "100",
        "capacity": 40,
    },
    
    # 200-Level Core Technical Courses
    {
        "code": "WD201",
        "title": "Web Development I: HTML5, CSS3 & Modern JS (ការអភិវឌ្ឍគេហទំព័រ ១)",
        "description": "Responsive UI design, flexbox/grid layouts, Bootstrap 5 framework, and modern client-side JavaScript DOM manipulation.",
        "credits": 3,
        "level": "200",
        "capacity": 40,
    },
    {
        "code": "DB202",
        "title": "Database Systems & Relational SQL (ប្រព័ន្ធមូលដ្ឋានទិន្នន័យ និង SQL)",
        "description": "Relational schema design, normalization, complex SQL joins, indexing, transaction management, and SQLite/PostgreSQL usage.",
        "credits": 3,
        "level": "200",
        "capacity": 40,
    },
    {
        "code": "NET203",
        "title": "Computer Networking & Cisco CCNA Fundamentals (មូលដ្ឋានបណ្តាញកុំព្យូទ័រ)",
        "description": "OSI & TCP/IP models, IP subnetting, VLANs, routing protocols, switches, and practical packet tracer labs.",
        "credits": 3,
        "level": "200",
        "capacity": 35,
    },
    {
        "code": "CS204",
        "title": "Data Structures & Algorithm Design (ទម្រង់ទិន្នន័យ និងក្បួនដោះស្រាយ)",
        "description": "Linked lists, stacks, queues, binary search trees, hash tables, sorting algorithms, and Big-O computational complexity.",
        "credits": 3,
        "level": "200",
        "capacity": 35,
    },
    {
        "code": "PY205",
        "title": "Python Programming for Applications (ការសរសេរកម្មវិធី Python កម្រិតខ្ពស់)",
        "description": "Object-oriented Python, decorators, file I/O, regex, web scraping, and automated scripting for administrative tasks.",
        "credits": 3,
        "level": "200",
        "capacity": 40,
    },
    {
        "code": "OS206",
        "title": "Linux Server Administration (ការគ្រប់គ្រងប្រព័ន្ធប្រតិបត្តិការ Linux)",
        "description": "Linux terminal mastery, bash shell scripting, user permissions, systemd services, SSH hardening, and Apache/Nginx web server setup.",
        "credits": 3,
        "level": "200",
        "capacity": 35,
    },

    # 300-Level Advanced Application Development
    {
        "code": "WD301",
        "title": "Web Development II: Django Framework & REST APIs (គេហទំព័រ Django & APIs)",
        "description": "Backend engineering with Django 4.2+, MVT architecture, Django REST Framework, token authentication, and full-stack integration.",
        "credits": 4,
        "level": "300",
        "capacity": 40,
    },
    {
        "code": "MOB302",
        "title": "Mobile App Development with Flutter & Dart (ការអភិវឌ្ឍកម្មវិធី Flutter)",
        "description": "Cross-platform mobile applications for Android and iOS using Flutter SDK, state management with Riverpod, and REST API consumption.",
        "credits": 4,
        "level": "300",
        "capacity": 35,
    },
    {
        "code": "DB303",
        "title": "Advanced Database: PostgreSQL & NoSQL MongoDB (ប្រព័ន្ធទិន្នន័យកម្រិតខ្ពស់)",
        "description": "Enterprise PostgreSQL database tuning, stored procedures, triggers, JSONB documents, and MongoDB document clustering.",
        "credits": 3,
        "level": "300",
        "capacity": 35,
    },
    {
        "code": "SEC304",
        "title": "Cyber Security Fundamentals & Ethical Hacking (សន្តិសុខព័ត៌មាន Cyber Security)",
        "description": "Network penetration testing, vulnerability assessment, cryptography, OWASP Top 10 vulnerabilities, and defense strategies.",
        "credits": 3,
        "level": "300",
        "capacity": 35,
    },
    {
        "code": "SE305",
        "title": "Software Engineering & Agile Methodologies (វិស្វកម្មផ្នែកទន់ និង Agile)",
        "description": "Software development life cycle, Scrum/Kanban frameworks, UML modeling, Git version control workflows, and CI/CD pipelines.",
        "credits": 3,
        "level": "300",
        "capacity": 40,
    },
    {
        "code": "CLOUD306",
        "title": "Cloud Computing: AWS Architecture & Docker (បច្ចេកវិទ្យា Cloud & Docker)",
        "description": "Cloud virtualization, Amazon EC2, S3 storage, Docker containerization, microservices deployment, and serverless compute.",
        "credits": 4,
        "level": "300",
        "capacity": 35,
    },

    # 400-Level Specialization & Capstone Courses
    {
        "code": "AI401",
        "title": "Artificial Intelligence & Machine Learning (បញ្ញាសិប្បនិម្មិត AI & Machine Learning)",
        "description": "Supervised and unsupervised learning, regression, classification, neural networks, scikit-learn, and computer vision with OpenCV.",
        "credits": 4,
        "level": "400",
        "capacity": 30,
    },
    {
        "code": "DS402",
        "title": "Data Science & Big Data Analytics (វិទ្យាសាស្ត្រទិន្នន័យ Data Science)",
        "description": "Data wrangling with Pandas/NumPy, exploratory data visualization with Matplotlib/Seaborn, and predictive statistical analytics.",
        "credits": 4,
        "level": "400",
        "capacity": 30,
    },
    {
        "code": "NET403",
        "title": "Enterprise Network Security & Firewalls (សន្តិសុខបណ្តាញកម្រិតខ្ពស់)",
        "description": "Next-generation firewalls, VPN tunnels, intrusion detection/prevention systems (IDS/IPS), and enterprise network monitoring.",
        "credits": 3,
        "level": "400",
        "capacity": 30,
    },
    {
        "code": "IOT404",
        "title": "Internet of Things (IoT) & Smart Devices (ប្រព័ន្ធ IoT និងឧបករណ៍ឆ្លាតវៃ)",
        "description": "Sensor interfacing with Raspberry Pi and ESP32, MQTT protocols, cloud IoT telemetry dashboards, and smart home automation.",
        "credits": 3,
        "level": "400",
        "capacity": 30,
    },
    {
        "code": "MOB405",
        "title": "Advanced Mobile Engineering: iOS Swift & Kotlin (កម្មវិធីទូរស័ព្ទកម្រិតខ្ពស់)",
        "description": "Native mobile development paradigms, memory management, background services, push notifications, and app store deployment.",
        "credits": 3,
        "level": "400",
        "capacity": 30,
    },
    {
        "code": "PM406",
        "title": "IT Project Management & Professional Ethics (ការគ្រប់គ្រងគម្រោង IT)",
        "description": "Project charter creation, cost estimation, risk matrices, stakeholder management, Cambodian intellectual property laws, and professional IT ethics.",
        "credits": 3,
        "level": "400",
        "capacity": 45,
    },
    {
        "code": "QA407",
        "title": "Software Quality Assurance & Automated Testing (ការធានាគុណភាពផ្នែកទន់)",
        "description": "Unit testing, integration testing, end-to-end automation with Selenium/Playwright, test-driven development (TDD), and performance load testing.",
        "credits": 3,
        "level": "400",
        "capacity": 35,
    },
    {
        "code": "UI408",
        "title": "UI/UX Design Systems & Human-Computer Interaction (ការរចនា UI/UX)",
        "description": "User research, wireframing, high-fidelity interactive prototyping in Figma, accessibility standards (WCAG), and usability testing.",
        "credits": 3,
        "level": "400",
        "capacity": 35,
    },
    {
        "code": "CAP409",
        "title": "IT Capstone Graduation Project (គម្រោងបញ្ចប់ការសិក្សាផ្នែកព័ត៌មានវិទ្យា)",
        "description": "Final graduation capstone project where student teams plan, architect, develop, and present a complete production software solution.",
        "credits": 4,
        "level": "400",
        "capacity": 50,
    },
]

KHMER_NOTES = [
    "លទ្ធផលសិក្សាល្អប្រសើរណាស់ (Outstanding academic performance)",
    "ការចូលរៀនទៀងទាត់ និងសកម្មក្នុងថ្នាក់ (Regular attendance and active in class)",
    "ការប្រឡងបញ្ចប់វគ្គទទួលបានពិន្ទុខ្ពស់ (High score on final examination)",
    "កិច្ចការស្រាវជ្រាវធ្វើបានល្អណាស់ (Very well-researched project assignment)",
    "មានការយល់ដឹងខ្ពស់លើការសរសេរកូដ (Strong grasp of programming concepts)",
    "សិស្សឆ្លាត និងមានភាពច្នៃប្រឌិត (Smart student with great creativity)",
    "ខិតខំប្រឹងប្រែងរៀនសូត្របានល្អ (Good effort and consistent study habit)",
    "ការងារក្រុមសហការបានល្អ (Great teamwork and peer collaboration)",
    "ត្រូវការអនុវត្តបន្ថែមលើលំហាត់កូដ (Needs additional coding practice)",
    "ការចូលរួមមធ្យម គួរព្យាយាមបន្ថែម (Average attendance, can improve more)",
]

def generate_cambodian_phone():
    prefix = random.choice(PHONE_PREFIXES)
    number = random.randint(100000, 999999)
    return f"{prefix}{number}"

def run_seed(num_students=1000):
    print("=" * 65)
    print("🚀 Build Bright University (BBU) - Seeding Khmer IT Data")
    print(f"🎯 Target: {num_students} Students, 25 IT Courses, 2,500+ Enrollments")
    print("=" * 65)

    with transaction.atomic():
        # 1. Create Instructors
        print("\n[1/4] 👨‍🏫 Creating IT Faculty Instructors...")
        instructor_objs = []
        default_pw_hash = make_password("BbuFaculty@2026")
        
        for username, first_name, last_name, email in INSTRUCTORS_DATA:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": default_pw_hash,
                    "is_staff": True,
                }
            )
            instructor_objs.append(user)
        print(f"      ✅ {len(instructor_objs)} Instructors ready.")

        # 2. Create Courses
        print("\n[2/4] 📚 Creating BBU IT Courses...")
        course_objs = []
        base_start = date(2024, 1, 15)
        base_end = date(2024, 6, 15)

        for i, c_data in enumerate(IT_COURSES_DATA):
            instructor = instructor_objs[i % len(instructor_objs)]
            course, created = Course.objects.update_or_create(
                code=c_data["code"],
                defaults={
                    "title": c_data["title"],
                    "description": c_data["description"],
                    "instructor": instructor,
                    "credits": c_data["credits"],
                    "level": c_data["level"],
                    "capacity": c_data["capacity"],
                    "status": "ACTIVE",
                    "start_date": base_start,
                    "end_date": base_end,
                }
            )
            course_objs.append(course)
        print(f"      ✅ {len(course_objs)} IT Courses configured.")

        # 3. Create Students (Batch Generation)
        print(f"\n[3/4] 🎓 Generating {num_students} Khmer Student Records...")
        
        # Determine existing student count for unique IDs
        existing_students = set(Student.objects.values_list('student_id', flat=True))
        existing_usernames = set(User.objects.values_list('username', flat=True))
        
        student_pw_hash = make_password("Student@123456")
        
        new_users = []
        user_meta = [] # Store student metadata associated with user
        
        id_counter = 1
        current_year = 2024
        
        for _ in range(num_students):
            # Generate unique student ID (e.g. BBU-2024-0001)
            while True:
                student_id = f"BBU-{current_year}-{id_counter:04d}"
                id_counter += 1
                if student_id not in existing_students:
                    existing_students.add(student_id)
                    break

            # Gender selection
            gender_roll = random.random()
            if gender_roll < 0.49:
                gender = "M"
                first_name_en, first_name_kh = random.choice(KHMER_MALE_FIRST_NAMES)
            elif gender_roll < 0.98:
                gender = "F"
                first_name_en, first_name_kh = random.choice(KHMER_FEMALE_FIRST_NAMES)
            else:
                gender = "O"
                first_name_en, first_name_kh = random.choice(KHMER_MALE_FIRST_NAMES)

            last_name_en, last_name_kh = random.choice(KHMER_LAST_NAMES)
            
            # Primary Khmer name (Last Name First Name in Khmer tradition)
            khmer_name = f"{last_name_kh} {first_name_kh}"
            first_name = first_name_en
            last_name = last_name_en

            # Unique username
            clean_first = first_name_en.lower()
            clean_last = last_name_en.lower()
            username = f"{clean_last}_{clean_first}_{id_counter}"
            while username in existing_usernames:
                username = f"{clean_last}_{clean_first}_{random.randint(1000, 99999)}"
            existing_usernames.add(username)

            email = f"{clean_last}.{clean_first}{id_counter}@student.bbu.edu.kh"

            # Birth date (18 - 25 years old)
            dob_year = random.randint(1999, 2005)
            dob_month = random.randint(1, 12)
            dob_day = random.randint(1, 28)
            dob = date(dob_year, dob_month, dob_day)

            # Location
            city_en, city_kh = random.choice(CAMBODIAN_CITIES)
            city = f"{city_en} ({city_kh})"
            address = f"{random.randint(1, 450)}, {random.choice(KHMER_STREET_ADDRESSES)}"
            phone = generate_cambodian_phone()
            
            # User object
            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=student_pw_hash,
                is_active=True,
            )
            new_users.append(user)
            user_meta.append({
                "student_id": student_id,
                "khmer_name": khmer_name,
                "date_of_birth": dob,
                "gender": gender,
                "phone_number": phone,
                "address": address,
                "city": city,
                "country": "Cambodia (កម្ពុជា)",
                "is_active": random.random() > 0.04, # 96% active
            })

        print("      📦 Bulk saving User accounts...")
        User.objects.bulk_create(new_users, batch_size=500)

        # Retrieve created users to get their DB primary keys
        created_usernames = [u.username for u in new_users]
        user_map = {u.username: u for u in User.objects.filter(username__in=created_usernames)}

        # Prepare Student objects
        student_objs = []
        for user_item, meta in zip(new_users, user_meta):
            user_inst = user_map[user_item.username]
            student = Student(
                user=user_inst,
                student_id=meta["student_id"],
                khmer_name=meta["khmer_name"],
                date_of_birth=meta["date_of_birth"],
                gender=meta["gender"],
                phone_number=meta["phone_number"],
                address=meta["address"],
                city=meta["city"],
                country=meta["country"],
                gpa=Decimal("0.00"),
                is_active=meta["is_active"],
            )
            student_objs.append(student)

        print("      📦 Bulk saving Student profiles...")
        Student.objects.bulk_create(student_objs, batch_size=500)
        
        # Retrieve saved students
        saved_students = list(Student.objects.filter(student_id__in=[s.student_id for s in student_objs]))
        print(f"      ✅ {len(saved_students)} Students successfully created.")

        # 4. Assign Course Enrollments
        print("\n[4/4] 📝 Assigning Course Enrollments & Computing Grades...")
        enrollment_objs = []
        student_gpa_map = {s.id: [] for s in saved_students}

        for student in saved_students:
            # Each student takes 2 to 4 courses randomly
            num_courses = random.randint(2, 4)
            chosen_courses = random.sample(course_objs, num_courses)

            for course in chosen_courses:
                status_roll = random.random()
                
                if status_roll < 0.70:
                    # 70% Completed with scores & calculated grades
                    status = "COMPLETED"
                    # Realistic grade distribution centered around 75-85
                    score = round(Decimal(str(random.gauss(80, 11))), 2)
                    score = max(Decimal("52.00"), min(Decimal("99.50"), score))
                    
                    if score >= 90:
                        grade = "A"
                    elif score >= 80:
                        grade = "B"
                    elif score >= 70:
                        grade = "C"
                    elif score >= 60:
                        grade = "D"
                    else:
                        grade = "F"
                        
                    attendance = round(Decimal(str(random.uniform(80.0, 100.0))), 1)
                    completed_date = course.end_date
                    notes = random.choice(KHMER_NOTES)
                    
                    # Store 4.0 scale points for GPA
                    grade_points = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}[grade]
                    student_gpa_map[student.id].append(grade_points)

                elif status_roll < 0.92:
                    # 22% Currently Enrolled
                    status = "ENROLLED"
                    score = None
                    grade = None
                    attendance = round(Decimal(str(random.uniform(85.0, 100.0))), 1)
                    completed_date = None
                    notes = "កំពុងសិក្សា (Currently in progress)"

                elif status_roll < 0.97:
                    # 5% Dropped
                    status = "DROPPED"
                    score = None
                    grade = None
                    attendance = round(Decimal(str(random.uniform(40.0, 70.0))), 1)
                    completed_date = None
                    notes = "សុំឈប់ដោយសារមូលហេតុផ្ទាល់ខ្លួន (Dropped due to personal reasons)"

                else:
                    # 3% Suspended
                    status = "SUSPENDED"
                    score = None
                    grade = None
                    attendance = round(Decimal(str(random.uniform(30.0, 60.0))), 1)
                    completed_date = None
                    notes = "ព្យួរការសិក្សាបណ្តោះអាសន្ន (Study temporarily suspended)"

                enrollment = Enrollment(
                    student=student,
                    course=course,
                    status=status,
                    score=score,
                    grade=grade,
                    attendance_percentage=attendance,
                    completed_date=completed_date,
                    notes=notes,
                )
                enrollment_objs.append(enrollment)

        print(f"      📦 Bulk saving {len(enrollment_objs)} Enrollments...")
        Enrollment.objects.bulk_create(enrollment_objs, batch_size=1000)
        print(f"      ✅ {len(enrollment_objs)} Enrollments created.")

        # Update student GPAs based on completed courses
        print("\n📊 Updating Student GPAs...")
        students_to_update = []
        for student in saved_students:
            points = student_gpa_map.get(student.id, [])
            if points:
                calc_gpa = round(sum(points) / len(points), 2)
            else:
                calc_gpa = Decimal("0.00")
            student.gpa = Decimal(str(calc_gpa))
            students_to_update.append(student)

        Student.objects.bulk_update(students_to_update, ['gpa'], batch_size=500)
        print(f"      ✅ {len(students_to_update)} Student GPAs computed and saved.")

    print("\n" + "=" * 65)
    print("🎉 DATA SEEDING COMPLETE!")
    print(f"👥 Total Students in System:    {Student.objects.count():,}")
    print(f"📚 Total IT Courses in System: {Course.objects.count():,}")
    print(f"📝 Total Enrollments in System:{Enrollment.objects.count():,}")
    print(f"🔑 Standard Student Password:   Student@123456")
    print(f"🔑 Faculty / Admin Password:    BbuFaculty@2026")
    print("=" * 65)

if __name__ == '__main__':
    count = 1000
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            pass
    run_seed(count)
