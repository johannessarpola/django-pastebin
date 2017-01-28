from django.contrib import admin

# Register your models here.
from .models import Paste, User, Duration

admin.site.register(Paste)
admin.site.register(Duration)