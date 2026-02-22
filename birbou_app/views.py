from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Lecture, Review
from .forms import CourseForm, LectureForm, ReviewForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Course
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course  # Use .models since Course is in this app



@login_required(login_url='/accounts/login/')
def home_view(request):
    public_courses = Course.objects.filter(is_public=True).order_by('-updated_at')
    private_courses = Course.objects.filter(is_public=False).order_by('-updated_at')
    
    return render(request, 'home.html', {
        'public_courses': public_courses,
        'private_courses': private_courses
    })

@login_required(login_url='/accounts/login/')
def professor_dashboard(request):
    if not request.user.groups.filter(name='professor').exists():
        return redirect('home')
    
    courses = Course.objects.filter(professor=request.user)
    course_form = CourseForm()
    
    return render(request, 'professor_dashboard.html', {
        'courses': courses,
        'course_form': course_form
    })

# Reolaced by upload_course
# @login_required(login_url='/accounts/login/')
# def create_course(request):
#     if not request.user.groups.filter(name='professor').exists():
#         return redirect('home')
#
#     if request.method == 'POST':
#         form = CourseForm(request.POST)
#         if form.is_valid():
#             course = form.save(commit=False)
#             course.professor = request.user
#             course.save()
#             return redirect('professor_dashboard')
#     return redirect('professor_dashboard')

@login_required(login_url='/accounts/login/')
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_owner = course.professor == request.user
    # Check if the current user is enrolled in the course
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = course.students.filter(id=request.user.id).exists()

    # 1. Private Course Logic for non-owners and non-enrolled students
    if not is_owner and not is_enrolled and not course.is_public:
        if course.password:
            session_key = f'course_unlocked_{course.id}'

            # Check if they are submitting the password
            if request.method == 'POST' and 'course_password' in request.POST:
                entered_password = request.POST.get('course_password')
                if entered_password == course.password:
                    request.session[session_key] = True  # Unlock for this session
                else:
                    return render(request, 'course_password_prompt.html', {
                        'course': course,
                        'error': 'Invalid password. Please try again.'
                    })

            # Redirect to password prompt if not unlocked yet
            if not request.session.get(session_key):
                return render(request, 'course_password_prompt.html', {'course': course})
        else:
            # Private course with no password set is locked
            return render(request, 'course_locked.html', {'course': course})
    # Check if a review was submitted
    if request.method == 'POST' and 'submit_review' in request.POST and is_enrolled:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()
            return redirect('course_detail', course_id=course.id)
    else:
        review_form = ReviewForm()

    if request.method == 'POST' and is_owner and 'submit_lecture' in request.POST:
        lecture_form = LectureForm(request.POST, request.FILES)
        if lecture_form.is_valid():
            lecture = lecture_form.save(commit=False)
            lecture.course = course
            lecture.save()
            return redirect('course_detail', course_id=course.id)
    else:
        lecture_form = LectureForm()

    # Check if the user already reviewed the course
    user_review = None
    if request.user.is_authenticated:
        user_review = course.reviews.filter(user=request.user).first()

    return render(request, 'course_detail.html', {
        'course': course,
        'lectures': course.lectures.all(),
        'lecture_form': lecture_form,
        'review_form': review_form,
        'user_review': user_review,
        'reviews': course.reviews.all(),
        'is_owner': is_owner,
        'is_enrolled': is_enrolled
    })

@login_required(login_url='/accounts/login/')
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.professor != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'edit_course.html', {'form': form, 'course': course})

@login_required(login_url='/accounts/login/')
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.professor != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        course.delete()
        return redirect('professor_dashboard')
    
    return render(request, 'confirm_delete.html', {'object': course, 'type': 'Course'})

@login_required(login_url='/accounts/login/')
def edit_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    if lecture.course.professor != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        form = LectureForm(request.POST, request.FILES, instance=lecture)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=lecture.course.id)
    else:
        form = LectureForm(instance=lecture)
    
    return render(request, 'edit_lecture.html', {'form': form, 'lecture': lecture})

@login_required(login_url='/accounts/login/')
def delete_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    if lecture.course.professor != request.user:
        return redirect('home')
    
    course_id = lecture.course.id
    if request.method == 'POST':
        lecture.delete()
        return redirect('course_detail', course_id=course_id)
    
    return render(request, 'confirm_delete.html', {'object': lecture, 'type': 'Lecture'})

@login_required(login_url='/accounts/login/')
def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    # Check if user has access to this course (e.g. is professor or enrolled student)
    # For now, we allow access to all logged in users, or restrict to professor if we wanted.
    # Given previous logic, let's keep it open for logged in users to view.
    
    is_owner = lecture.course.professor == request.user
    
    return render(request, 'lecture_detail.html', {
        'lecture': lecture,
        'course': lecture.course,
        'is_owner': is_owner
    })


@login_required(login_url='/accounts/login/')
def upload_course(request):
    if not request.user.groups.filter(name='professor').exists():
        return redirect('home')

    if request.method == 'POST':
        # Added request.FILES so images actually upload
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.professor = request.user
            course.save()
            return redirect('professor_dashboard')
    else:
        form = CourseForm()

    return render(request, 'upload_course.html', {'form': form})


# You can now delete the old 'def create_course' to avoid confusion.

import json

@require_POST
def toggle_course_visibility(request, course_id):
    course = get_object_or_404(Course, id=course_id, professor=request.user)
    
    try:
        body_text = request.body.decode('utf-8').strip()
        print("DEBUG: Raw request.body inside toggle_course_visibility:", body_text)
        if not body_text:
            data = {}
        else:
            data = json.loads(body_text)
            
        is_public = data.get('is_public', not course.is_public)
        password = data.get('password', '')
        
        course.is_public = is_public
        
        if not is_public:
            course.password = password
        else:
            course.password = ''
            
        course.save()
        return JsonResponse({'status': 'success', 'is_public': course.is_public})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)


@login_required(login_url='/accounts/login/')
def professor_dashboard(request):
    # This matches the new column you just created
    courses = Course.objects.filter(professor=request.user).order_by('-updated_at')

    return render(request, 'professor_dashboard.html', {
        'courses': courses,
    })


@login_required
def enroll_in_course(request, course_id):
    # Fetch the course
    course = get_object_or_404(Course, id=course_id)

    # Check if the user is already enrolled
    if request.user not in course.students.all():
        course.students.add(request.user)
        # We call save() to trigger the 'updated_at' timestamp
        # so it jumps to the top of your dashboard
        course.save()

    return redirect('course_detail', course_id=course.id)


@login_required
def unenroll_from_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.user in course.students.all():
        course.students.remove(request.user)
        course.save()

    return redirect('my_courses')


@login_required
def my_courses(request):
    if request.user.groups.filter(name='professor').exists():
         return redirect('professor_dashboard')
         
    enrolled_courses = request.user.enrolled_courses.all().order_by('-updated_at')
    
    return render(request, 'my_courses.html', {
        'enrolled_courses': enrolled_courses
    })

@login_required(login_url='/accounts/login/')
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    # Only allow the user who created the review to delete it
    if review.user == request.user:
        course_id = review.course.id
        review.delete()
        return redirect('course_detail', course_id=course_id)
    return redirect('home')