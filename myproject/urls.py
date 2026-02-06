"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
# from birbou_app.views import login_view, register_view
from django.shortcuts import redirect


# def home(request):
#     return render(request, 'login.html')  # commented those out, not necessary since accounts app handles login/signup


# function that redirects to login page
def redirect_to_login(request):
    return redirect("/accounts/login/")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login),  # root redirects to login page
    path('accounts/', include('accounts.urls')),  # if you catch accounts/, redirect to account views
]