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
        e_info.save()
        e_info.paste_count = 0