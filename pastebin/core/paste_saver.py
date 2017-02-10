from pastebin.core.paste_hasher import PasteHasher
from django.contrib.auth.models import User

from pastebin.core.paste_dates import PasteDates
from pastebin.models import PasteForm


class PasteSaver:
    def __init__(self):
        self.pd = PasteDates()
        self.ph = PasteHasher(1459, 8)
        super().__init__()

    def handle_saving(self, pf: PasteForm, u:User):
        entity = pf.save(commit=False)
        entity.creation_date = self.pd.now()
        entity.user = u
        entity.expiration = pf.cleaned_data['expiration']
        entity.expiry_date = self.pd.create_expiration_date(entity.expiration)
        entity.hash = self.ph.generate_hash(entity)
        print(entity.hash)
        pf.save(commit=True)
        return entity.hash

