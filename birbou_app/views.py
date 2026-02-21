from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Lecture
from .forms import CourseForm, LectureForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Course
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course  # Use .models since Course is in this app



@login_required(login_url='/accounts/login/')
def home_view(request):
    public_courses = Course.objects.filter(is_public=True)
    return render(request, 'home.html', {'courses': public_courses})

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

    # 1. Password Logic for non-owners
    if not is_owner and course.password:
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

    # 2. Existing Lecture Logic (Only owner can add lectures)
    if request.method == 'POST' and is_owner:
        form = LectureForm(request.POST, request.FILES)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.course = course
            lecture.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = LectureForm()

    return render(request, 'course_detail.html', {
        'course': course,
        'lectures': course.lectures.all(),
        'form': form,
        'is_owner': is_owner
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

@require_POST
def toggle_course_visibility(request, course_id):
    course = get_object_or_404(Course, id=course_id, professor=request.user)
    course.is_public = not course.is_public
    course.save()
    return JsonResponse({'status': 'success', 'is_public': course.is_public})


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

    return redirect('professor_dashboard')

def home_view(request):
    # Only show public courses to students/guests
    public_courses = Course.objects.filter(is_public=True).order_by('-updated_at')
    return render(request, 'home.html', {'courses': public_courses})