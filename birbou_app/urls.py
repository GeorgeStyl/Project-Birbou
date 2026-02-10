from django.urls import path
from . import views

urlpatterns = [
    # Αυτό θα αντιστοιχεί στο 127.0.0.1:8000/home/
    path('home/', views.home_view, name='home'),
    path('professor/dashboard/', views.professor_dashboard, name='professor_dashboard'),
    path('professor/create-course/', views.create_course, name='create_course'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('course/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('lecture/<int:lecture_id>/edit/', views.edit_lecture, name='edit_lecture'),
    path('lecture/<int:lecture_id>/delete/', views.delete_lecture, name='delete_lecture'),
    path('lecture/<int:lecture_id>/', views.lecture_detail, name='lecture_detail'),
    # path('professor/upload/', views.upload_course, name='upload_course'), # Deprecated
]