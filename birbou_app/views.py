from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Αυτό το view θα δείχνει την αρχική σελίδα μετά το login
@login_required(login_url='/accounts/login/')
def home_view(request):
    return render(request, 'home.html')