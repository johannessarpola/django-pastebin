from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=120)
    display_name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)

class Text(models.Model):
    text_field = models.TextField()
    date = models.DateField('date pasted')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


