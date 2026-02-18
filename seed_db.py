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

    # Create Courses
    print("Creating courses...")
    courses_data = [
        {
            "title": "Introduction to Algorithms",
            "description": "A fundamental course on algorithmic thinking and complexity analysis.",
            "professor": prof1
        },
        {
            "title": "Artificial Intelligence",
            "description": "Exploring the basics of AI, machine learning, and neural networks.",
            "professor": prof1
        },
        {
            "title": "Web Development with Django",
            "description": "Building robust web applications using the Django framework.",
            "professor": prof1
        },
        {
            "title": "Database Systems",
            "description": "Design and implementation of database management systems.",
            "professor": prof1
        }
    ]

    for data in courses_data:
        course = Course.objects.create(
            title=data["title"],
            description=data["description"],
            professor=data["professor"]
        )
        
        print(f"  Created course: {course.title}")
        
        
        for i in range(1, 6):
            Lecture.objects.create(
                course=course,
                title=f"Lecture {i}: {course.title} Part {i}",
                description=f"This is the detailed description for lecture {i} of {course.title}. In this lecture, we cover advanced topics and practical examples related to the course subject matter."
            )

    print("✅ Seeding completed successfully!")
    print("\nUsers created/verified (password: password123):")
    print("- Professor: prof_turing")
    print("- Student: student_ada")

if __name__ == '__main__':
    seed()
