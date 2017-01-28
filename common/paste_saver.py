from django.contrib.auth.models import User

from common.paste_dates import PasteDates
from common.paste_hasher import PasteHasher
from pastebin.models import PasteForm, Paste


class PasteSaver:
    def __init__(self):
        self.pd = PasteDates()
        self.ph = PasteHasher(1459, 8)
        super().__init__()

    def hande_saving(self, pf: PasteForm, u:User):
        entity = pf.save(commit=False)
        entity.creation_date = self.pd.current_date()
        entity.user = u
        entity.expiration_date = self.pd.expiration_date(pf.expiration_enum)
        entity.hash = self.ph.generate_hash(entity)


