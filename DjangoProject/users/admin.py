from django.contrib import admin
from .models import Profile, User

# Registered the models here.
admin.site.register(Profile)
admin.site.register(User)