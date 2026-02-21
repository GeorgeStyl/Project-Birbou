from django import forms
from .models import Course, Lecture

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'is_public', 'password']
        widgets = {
            'password': forms.PasswordInput(render_value=True, attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Optional Password'
            }),
        }


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'file', 'video', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lecture Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Lecture Description', 'rows': 3}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
