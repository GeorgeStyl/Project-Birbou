from django.urls import path
from .views import login_view, signup_view, logout_view
from . import views 
from django.contrib.auth.models import User, Group  



urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='register'), # Άλλαξε το 'signup' σε 'register' εδώ
    path('logout/', views.logout_view, name='logout'),
    path('guest-login/', views.guest_login_view, name='guest_login'), 
]