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
    print("Creating professor...")
    prof1, created = User.objects.get_or_create(username='prof_turing', email='turing@example.com')
    if created:
        prof1.set_password('password123')
        prof1.first_name = 'Alan'
        prof1.last_name = 'Turing'
        prof1.save()
        prof1.groups.add(prof_group)
    else:
        prof1.groups.add(prof_group)

    # Create Student
    print("Creating students...")
    student1, created = User.objects.get_or_create(username='student_ada', email='ada@example.com')
    if created:
        student1.set_password('password123')
        student1.first_name = 'Ada'
        student1.last_name = 'Lovelace'
        student1.save()
        student1.groups.add(student_group)

    # Create Courses with Optional Passwords
    print("Creating courses...")
    courses_data = [
        {
            "title": "Introduction to Algorithms",
            "description": "A fundamental course on algorithmic thinking and complexity analysis.",
            "professor": prof1,
            "image": "courses/introduction_to_algorithms.png",
            "password": "algo_secret_2026", # Added Password
            "is_public": True
        },
        {
            "title": "Artificial Intelligence",
            "description": "Exploring the basics of AI, machine learning, and neural networks.",
            "professor": prof1,
            "image": "courses/artificial_intelligence.png",
            "password": "ai_mastery_99",    # Added Password
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
    print("\nUsers created/verified (password: password123):")
    print("- Professor: prof_turing")
    print("- Student:   student_ada")

if __name__ == '__main__':
    seed()