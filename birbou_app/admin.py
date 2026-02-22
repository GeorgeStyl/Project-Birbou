from django.contrib import admin
from .models import Course, Lecture, Review

admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Review)
