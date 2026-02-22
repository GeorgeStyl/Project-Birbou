from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home_view, name='home'),

    # * ##############################
    # * PRODESSOR DASHBOARD
    # * ##############################
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/delete/', views.delete_course, name='confirm_delete'),
    path('course/upload/', views.upload_course, name='upload_course'),
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),

    path('lecture/<int:lecture_id>/', views.lecture_detail, name='lecture_detail'),
    path('lecture/<int:lecture_id>/edit/', views.edit_lecture, name='edit_lecture'),
    path('lecture/<int:lecture_id>/delete/', views.delete_lecture, name='delete_lecture'),
    path('course/toggle-visibility/<int:course_id>/', views.toggle_course_visibility, name='toggle_visibility'),
    path('course/<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),


    # * ##############################
    # * STUDENTS
    # * #############################
    path('course/<int:course_id>/unenroll/', views.unenroll_from_course, name='unenroll_from_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)