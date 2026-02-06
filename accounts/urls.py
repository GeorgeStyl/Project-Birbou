from django.urls import path
from .views import login_view, signup_view, logout_view

urlpatterns = [
    path("login/", login_view, name="login"),  # go to login view
    path("register/", signup_view, name="register"),  # go to register view
    path("logout/", logout_view, name="logout"),  # go to logout view, currently redirects to root which redirects
                                                        # to login view
]
