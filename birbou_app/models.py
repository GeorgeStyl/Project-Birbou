from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)  # This is key for the "Last Private = First" rule

    class Meta:
        ordering = ['-updated_at']  # Always serves the most recently updated courses first


    def __str__(self):
        return self.title

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='lectures/files/', blank=True, null=True)
    video = models.FileField(upload_to='lectures/videos/', blank=True, null=True)
    image = models.ImageField(upload_to='lectures/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
