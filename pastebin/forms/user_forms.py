from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from pastebin.models import UserExtraInfo


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ExtraEditForm(ModelForm):
    class Meta:
        model = UserExtraInfo
        fields = ['bio']
        labels = {
            'bio' : ('Your bio')

        }
        help_texts = {
            'bio' :'Let us know more about you'
        }

    def save_with_user(self, user):
        from pastebin.core.user_retriever import UserRetriever
        e_info = UserRetriever().get_user_extra_info_if_exists(user)
        if e_info is None:
            e_info = UserExtraInfo()
            e_info.paste_count = 0
        e_info.bio = self.cleaned_data['bio']
        e_info.save()

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        labels = {
            'email' :('Your email'),
            'first_name' :('Your first name'),
            'last_name' :('Your last name'),
        }

    def save_with_request(self, request):
        user = request.user
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.save(commit=True)