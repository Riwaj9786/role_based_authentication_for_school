from django.contrib import admin
from role_app import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Student)
