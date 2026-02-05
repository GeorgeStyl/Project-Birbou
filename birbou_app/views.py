from django.shortcuts import render

def login_view(request):
    if request.method == "POST":
    
        user_val = request.POST.get('username')
        pass_val = request.POST.get('password')
        
        
        # If checked, it returns 'on'. If NOT checked, it returns None.
        remember = request.POST.get('remember_me') 

        # For debugging
        print(f"Login attempt: User={user_val}, Pass={pass_val}, Remember={remember}")

        # Re-render
        return render(request, 'base.html')

    # If the user is just visiting the page (GET)
    return render(request, 'login.html')


# Redirect if signup button is clicked
def register_view(request):
    if request.method == "POST":
        role = request.POST.get('role')
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password') 

        # For debugging: Print the received data to the console
        print("\n--- NEW USER REGISTERED ---")
        print(f"Role:      {role}")
        print(f"Full Name: {name}")
        print(f"Email:     {email}")
        print(f"Password:  {password}")
        print("---------------------------\n")

        # After printing, redirect or stay on the page
        return render(request, 'register.html')
    
    return render(request, 'register.html')