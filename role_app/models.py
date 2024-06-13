import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.utils.text import slugify


class User(AbstractUser):
    user_id = models.CharField(unique=True, max_length=15)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    date_of_birth = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = str(uuid.uuid4())[:15]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    

class Student(models.Model):
    registration_number = models.CharField(max_length=30, unique=True, null=True, editable=False)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    batch_year = models.CharField(max_length=4)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    date_of_birth = models.DateField()
    email = models.EmailField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Link to User model

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.registration_number:
            count = Student.objects.filter(batch_year=self.batch_year).count() + 1
            registration_number = f"{self.batch_year}-{count}"
            self.registration_number = slugify(registration_number)
        super().save(*args, **kwargs)
