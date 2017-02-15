class UserSaver:

    def __init__(self):
        import logging
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def handle_saving(self, request):
        from pastebin.forms.user_forms import RegistrationForm
        registration_form = RegistrationForm(request.POST)
        if registration_form is not None:
            entity = registration_form.save(commit=True) # TODO Should probably log if there's problems
            return entity
        else:
            self.logger.warning("Couldn't create user from form")
            return None
