import os
import django
import random
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User, Group
from birbou_app.models import Course, Lecture

def seed():
    print("🌱 Seeding data...")

    # Clear existing data to ensure clean state
    print("Clearing existing data...")
    Lecture.objects.all().delete()
    Course.objects.all().delete()

    # Create Groups
    print("Creating groups...")
    prof_group, _ = Group.objects.get_or_create(name='professor')
    student_group, _ = Group.objects.get_or_create(name='student')

    # Create Professor
    print("Creating professors...")
    prof1, _ = User.objects.get_or_create(username='prof_turing', email='turing@example.com')
    prof1.set_password('password123')
    prof1.first_name = 'Alan'
    prof1.last_name = 'Turing'
    prof1.save()
    prof1.groups.add(prof_group)

    chris_prof, _ = User.objects.get_or_create(username='chris_prof', email='chris_prof@example.com')
    chris_prof.set_password('pass123456')
    chris_prof.first_name = 'Chris'
    chris_prof.last_name = 'Professor'
    chris_prof.save()
    chris_prof.groups.add(prof_group)

    # Create Student
    print("Creating students...")
    student1, _ = User.objects.get_or_create(username='student_ada', email='ada@example.com')
    student1.set_password('password123')
    student1.first_name = 'Ada'
    student1.last_name = 'Lovelace'
    student1.save()
    student1.groups.add(student_group)

    chris_tzamp, _ = User.objects.get_or_create(username='chris_tzamp', email='chris@example.com')
    chris_tzamp.set_password('pass123456')
    chris_tzamp.first_name = 'Chris'
    chris_tzamp.last_name = 'Tzamp'
    chris_tzamp.save()
    chris_tzamp.groups.add(student_group)

    # Create Courses with Optional Passwords
    print("Creating courses...")
    courses_data = [
        {
            "title": "Introduction to Algorithms",
            "description": "A fundamental course on algorithmic thinking and complexity analysis.",
            "professor": prof1,
            "image": "courses/introduction_to_algorithms.png",
            "password": "pass12345", # Added Password
            "is_public": True
        },
        {
            "title": "Artificial Intelligence",
            "description": "Exploring the basics of AI, machine learning, and neural networks.",
            "professor": prof1,
            "image": "courses/artificial_intelligence.png",
            "password": "pass12345",    # Added Password
            "is_public": True
        },
        {
            "title": "Web Development with Django",
            "description": "Building robust web applications using the Django framework.",
            "professor": prof1,
            "image": "courses/django.png",
            "password": None,
            "is_public": True
        },
        {
            "title": "Database Systems",
            "description": "Design and implementation of database management systems.",
            "professor": prof1,
            "image": "courses/database.png",
            "password": None,
            "is_public": True
        },
        {
            "title": "Advanced Python Programming",
            "description": "Mastering Python for data science, web development and automation.",
            "professor": chris_prof,
            "image": None,
            "password": None,
            "is_public": True
        },
        {
            "title": "Machine Learning Foundations",
            "description": "Introduction to core ML concepts, algorithms and practical applications.",
            "professor": chris_prof,
            "image": None,
            "password": "pass12345",
            "is_public": True
        },
        {
            "title": "Cloud Computing with AWS",
            "description": "Learn to deploy, manage, and scale applications on Amazon Web Services.",
            "professor": chris_prof,
            "image": None,
            "password": None,
            "is_public": True
        },
        {
            "title": "Cybersecurity Fundamentals",
            "description": "Protecting systems, networks, and programs from digital attacks.",
            "professor": chris_prof,
            "image": None,
            "password": None,
            "is_public": True
        },
        {
            "title": "Data Structures in C++",
            "description": "Deep dive into memory management and complex data structures.",
            "professor": chris_prof,
            "image": None,
            "password": "pass12345",
            "is_public": True
        },
        {
            "title": "Mobile App Development",
            "description": "Creating cross-platform mobile applications using modern frameworks.",
            "professor": chris_prof,
            "image": None,
            "password": None,
            "is_public": True
        },
        {
            "title": "Private: Advanced React Patterns",
            "description": "Deep dive into advanced React concepts, hooks, and performance optimization.",
            "professor": chris_prof,
            "image": None,
            "password": "pass12345",
            "is_public": False
        },
        {
            "title": "Private: System Design Interview",
            "description": "Preparation for scalable system design interviews at FAANG companies.",
            "professor": chris_prof,
            "image": None,
            "password": "pass12345",
            "is_public": False
        },
        {
            "title": "Private: Ethical Hacking Workshop",
            "description": "Hands-on penetration testing and vulnerability assessment techniques.",
            "professor": chris_prof,
            "image": None,
            "password": "pass12345",
            "is_public": False
        },
        {
            "title": "Private: Next.js Full Stack App",
            "description": "Building a production-ready full-stack application with Next.js 14.",
            "professor": chris_prof,
            "image": None,
            "password": "pass12345",
            "is_public": False
        },
        {
            "title": "Private: Financial Analysis with Pandas",
            "description": "Using Python and Pandas for stock market analysis and algorithmic trading.",
            "professor": chris_prof,
            "image": None,
            "password": "pass12345",
            "is_public": False
        },
        {
            "title": "Private: Game Development with Godot",
            "description": "Creating 2D and 3D games from scratch using the Godot engine.",
            "professor": chris_prof,
            "image": None,
            "password": None, # Intentionally left empty to trigger the locked screen
            "is_public": False
        }
    ]

    print("\n--- Protected Course List ---")
    for data in courses_data:
        course = Course.objects.create(
            title=data["title"],
            description=data["description"],
            professor=data["professor"],
            image=data["image"],
            password=data.get("password"), # Assign password here
            is_public=data.get("is_public", False)
        )

        # Print the course name and password if it exists
        status = f"Locked (🔑: {course.password})" if course.password else "Open Access"
        print(f"Course: {course.title.ljust(30)} | Status: {status}")

        for i in range(1, 6):
            Lecture.objects.create(
                course=course,
                title=f"Lecture {i}: {course.title} Part {i}",
                description=f"Detailed description for lecture {i} of {course.title}."
            )

    print("\n✅ Seeding completed successfully!")
    print("\nUsers created/verified:")
    print("- Professor 1: prof_turing  | pass: password123")
    print("- Professor 2: chris_prof   | pass: pass123456")
    print("- Student 1:   student_ada  | pass: password123")
    print("- Student 2:   chris_tzamp  | pass: pass123456")

if __name__ == '__main__':
    seed()