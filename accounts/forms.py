from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ExtendedSignupForm(UserCreationForm):
    full_name = forms.CharField(
        label="Full Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'})
    )
    university = forms.CharField(
        label="University",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g. University of Crete'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "full_name", "email", "university")

    def save(self, commit=True):
        user = super().save(commit=False)
        name_parts = self.cleaned_data["full_name"].split(' ', 1)
        user.first_name = name_parts[0]
        user.last_name = name_parts[1] if len(name_parts) > 1 else ""
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
        return user