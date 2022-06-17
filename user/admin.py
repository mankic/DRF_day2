from django.contrib import admin
from .models import User, UserManager, UserProfile, Hobby

# Register your models here.
admin.site.register(User)
# admin.site.register(UserManager)
admin.site.register(UserProfile)
admin.site.register(Hobby)