from django.forms import ModelForm

from pastebin.models import Paste


class PasteForm(ModelForm):
    class Meta:
        model = Paste
        fields = ['text_field', 'expiration']
        labels = {
            'text_field': ('Paste'),
        }
        help_texts = {
            'text_field': 'Paste your text here and hit save',
            'expiration': 'Sets when the paste is expired and thus after it will be inaccessible and removed'
        }
        error_messages = {

        }