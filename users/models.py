from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    role = models.CharField(
        max_length=20, 
        choices=[('admin', 'Admin'), ('driver', 'Driver'), ('parent', 'Parent')], 
        default='admin'
    )
    bus_number = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    def __str__(self):
        return self.username


# Student Model
class Student(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': 'parent'}, 
        related_name="parent_students"
    )
    driver = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        limit_choices_to={'role': 'driver'}, 
        null=True, 
        blank=True, 
        related_name="driver_students"
    )
    bus_number = models.CharField(max_length=10, blank=True, null=True)  # Allow bus_number to be blank

    def save(self, *args, **kwargs):
        """Automatically set bus_number from parent or driver before saving."""
        if self.driver and self.driver.bus_number:
            self.bus_number = self.driver.bus_number  # Priority to driver's bus number
        elif self.parent and self.parent.bus_number:
            self.bus_number = self.parent.bus_number  # Otherwise, use parent's bus number
        
        super().save(*args, **kwargs)  # Call Django's default save method

    def __str__(self):
        return self.name

from django.db import models
from .models import User, Student

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.name} - {self.status} ({self.date})"
# ✅ Driver Attendance & Working Hours Model
class DriverAttendance(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})
    date = models.DateField(auto_now_add=True)
    login_time = models.DateTimeField(default=now)
    logout_time = models.DateTimeField(null=True, blank=True)
    total_hours = models.FloatField(null=True, blank=True)

    def calculate_hours(self):
        if self.logout_time:
            delta = self.logout_time - self.login_time
            self.total_hours = round(delta.total_seconds() / 3600, 2)
            self.save()

    def __str__(self):
        return f"{self.driver.username} - {self.date}"

import requests
from django.http import JsonResponse
from .models import User



from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Feedback(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks")
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[('open', 'Open'), ('closed', 'Closed')],
        default='open'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {self.parent.username} - {self.status}"
