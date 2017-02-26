class UserSaver:

    def __init__(self):
        import logging
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def handle_saving(self, request):
        from pastebin.forms.user_forms import RegistrationForm
        registration_form = RegistrationForm(request.POST)
        if registration_form is not None:
            user = registration_form.save(commit=True)
            self.save_extra_info(user)
            return user
        else:
            self.logger.warning("Couldn't create user from form")
            return None

    def save_extra_info(self, user):
        from pastebin.models import UserExtraInfo
        e_info = UserExtraInfo()
        e_info.user = user
        e_info.paste_count = 0
        e_info.save()

    def handle_edit_profile_forms(self, request):
        from pastebin.forms import user_forms
        if request.method == 'POST':
            extra_e_form = user_forms.ExtraEditForm(request.POST,instance=request.user)
            user_e_form = user_forms.UserEditForm(request.POST,instance=request.user)
            if extra_e_form.is_valid() and user_e_form.is_valid() and request.user.is_authenticated():
                user = user_e_form.save()
                extra_e_form.update(user)
                return "Ok"
            else:
                self.logger.error("Forms were invalid")
                return None
        else:
            self.logger.error("Forms were invalid ")
            return None