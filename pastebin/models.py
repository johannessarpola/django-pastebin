from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

class Duration(models.Model):
    Year, Month, Week, Day, Hour, FifteenMinutes = range(6)
    addition_minutes = models.BigIntegerField(default=15)

class Paste(models.Model):
    text_field = models.TextField()
    creation_date = models.DateField('creation date')
    expiry_date = models.DateField('expiration date')
    expiration_enum = models.OneToOneField(to=Duration, on_delete=None, default=Duration.FifteenMinutes)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash = models.CharField(max_length=20, default="undefined")

class PasteForm(ModelForm):
    class Meta:
        model = Paste
        fields = ['text_field', 'expiration_enum']
        labels = {
            'text_field': ('Paste'),
        }
        help_texts = {
            'text_field': ('Paste your text here'),
        }
        error_messages = {

        }

