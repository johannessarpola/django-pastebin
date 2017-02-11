class UserSaver:

    def __init__(self):
        import logging
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def handle_saving(self, request):
        from django.contrib.auth.forms import UserCreationForm
        userForm = UserCreationForm(request.POST)
        if userForm is not None:
            entity = userForm.save(commit=True) # TODO Should probably log if there's problems
            return entity
        else:
            self.logger.warning("Couldn't create user from form")
            return None
