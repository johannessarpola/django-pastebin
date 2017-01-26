from django.contrib import admin

# Register your models here.
from .models import Text, User

admin.site.register(Text)
admin.site.register(User)