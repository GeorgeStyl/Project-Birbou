from django.urls import path
from . import views

urlpatterns = [
    # Αυτό θα αντιστοιχεί στο 127.0.0.1:8000/home/
    path('home/', views.home_view, name='home'),
]