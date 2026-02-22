from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Create your models here.
from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True, help_text="Optional password to access the course")
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teaching_courses'
    )
    # This field tracks which users are signed into the course
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='enrolled_courses',
        blank=True
    )
    is_public = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            avg = sum([r.rating for r in reviews]) / reviews.count()
            return round(avg, 1) # Keep 1 decimal place
        return 0

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

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # Prevent a user from leaving multiple reviews for the same course
        unique_together = ('course', 'user')

    def __str__(self):
        return f"{self.user.username}'s review on {self.course.title}"
