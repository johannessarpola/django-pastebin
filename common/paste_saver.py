from django.contrib.auth.models import User

from common.paste_dates import PasteDates
from common.paste_hasher import PasteHasher
from pastebin.models import PasteForm, Paste


class PasteSaver:
    def __init__(self):
        self.pd = PasteDates()
        self.ph = PasteHasher(1459, 8)
        super().__init__()

    def handle_saving(self, pf: PasteForm, u:User):
        entity = pf.save(commit=False)
        entity.creation_date = self.pd.current_date()
        entity.user = u
        entity.expiry_date = self.pd.expiration_date(pf.cleaned_data['expiration'])
        entity.expiration = pf.cleaned_data['expiration']
        entity.hash = self.ph.generate_hash(entity)
        print(entity.hash)
        pf.save(commit=True)
        return entity.hash

