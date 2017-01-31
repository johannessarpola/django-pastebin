from pastebin.models import Paste
from common.paste_dates import PasteDates
import logging

class PasteRemover:
    def __init__(self):
        super().__init__()
        self.paste_dates = PasteDates()
        self.logger = logging.getLogger(__name__)

    def removeExpiredPastes(self):
        cur_dt = self.paste_dates.now()
        filtered = Paste.objects.filter(expiry_date__lte=cur_dt)
        self.logger.info("Found {} objects to be removed", len(filtered))
        filtered.delete()