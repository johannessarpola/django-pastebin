from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

class Duration(models.Model):
    Year, Month, Week, Day, Hour, FifteenMinutes = range(6)
    addition_minutes = models.BigIntegerField(default=15)
    description = models.CharField(max_length=100, default="undefined")

    def __str__(self):
        return self.description


class Paste(models.Model):
    text_field = models.TextField()
    creation_date = models.DateTimeField('creation date')
    expiry_date = models.DateTimeField('expiration date')
    expiration = models.ForeignKey(to=Duration, on_delete=None, default=Duration.FifteenMinutes)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hash = models.CharField(max_length=20, default="undefined")

    def to_json(self):
        from django.forms.models import model_to_dict
        return model_to_dict(self)

class PasteForm(ModelForm):
    class Meta:
        model = Paste
        fields = ['text_field', "expiration"]
        labels = {
            'text_field': ('Paste'),
        }
        help_texts = {
            'text_field': ('Paste your text here'),
        }
        error_messages = {

        }

