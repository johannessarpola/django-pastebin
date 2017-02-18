from django.contrib.auth.models import User
from pastebin.forms.paste_forms import PasteForm
from pastebin.models import Paste


class PasteSaver:
    def __init__(self):
        from pastebin.core.paste_hasher import PasteHasher
        from pastebin.core.paste_dates import PasteDates

        self.pd = PasteDates()
        self.ph = PasteHasher(1459, 8)
        super().__init__()
        import logging
        self.logger = logging.getLogger(__name__)

    def handle_saving(self, pf: PasteForm, user:User):
        paste = self.create_paste_from_form(form=pf, user=user)
        self.update_user_paste_stats(paste)
        print(paste.hash)
        pf.save(commit=True)
        return paste.hash

    def create_paste_from_form(self, form:PasteForm, user:User):
        entity = form.save(commit=False)
        entity.creation_date = self.pd.now()
        entity.user = user
        entity.expiration = form.cleaned_data['expiration']
        entity.expiry_date = self.pd.create_expiration_date_for_date(entity.creation_date, entity.expiration)
        entity.hash = self.ph.generate_hash(entity)
        return entity

    def update_user_paste_stats(self, paste:Paste):
        from pastebin.models import UserExtraInfo
        stats = None
        try:
            stats = UserExtraInfo.objects.get(user=paste.user)
            stats.paste_count += 1
        except UserExtraInfo.DoesNotExist:
            stats = UserExtraInfo()
            stats.user = paste.user
            stats.paste_count = 1
            stats.bio = "Undefined"
            self.logger.warning("Couldn't find extra info for user: {}".format(paste.user.id))
        stats.save()


def paste_from_request(request):
    user = request.user
    form = PasteForm(request.POST)
    if form.is_valid():
        ps = PasteSaver()
        hash = ps.handle_saving(form, user)
        return hash
    else:
        logger.warning("Received invalid form: {}".format(str(form)))
        return None