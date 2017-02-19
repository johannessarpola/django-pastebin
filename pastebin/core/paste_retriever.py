import numbers

from pastebin.models import Paste, Duration


class PasteRetriever:
    def __init__(self):
        import logging
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def get_by_hash(self, hash):
        pastes = self.get_by_hash_queryset(hash)
        if (len(pastes) > 0):
            self.logger.warning("There were multiple pastes for same hash")
            return pastes[0]
        else:
            return pastes

    def get_latest(self, amount):
        return Paste.objects.order_by('-creation_date')[:amount]

    def get_lastest_5(self):
        return self.get_latest(5)

    def get_lastest_10(self):
        return self.get_latest(10)

    def get_by_hash_json(self, hash):
        from django.core import serializers
        qs = self.get_by_hash_queryset(hash)
        rawjson = serializers.serialize('json',
                                        qs,
                                        ensure_ascii=False,
                                        fields=('text_field', 'creation_date', 'expiry_date', 'hash', 'user'))
        return rawjson  # TODO improve so that pk and model gets removed

    def get_by_hash_simplejson(self, hash):
        qs_result = self.get_by_hash(hash)
        dto = paste_to_dto(qs_result)
        return dto

    def get_by_hash_queryset(self, hash):
        return Paste.objects.filter(hash__exact=hash)

    def find_by(self, field_name: str, operand: str, field_value):
        '''
        Uses pure sql for dynamic retrieval
        :param field_name:
        :param operand:
        :param field_value:
        :return:
        '''
        if (operand == '='):
            # TODO For some reason this doesn't find anything if you use parameters even though it would work with a raw string query
            pastes = self.find_by_eq(field_name, field_value)
            for p in pastes:
                print(p)
                return p
        else:
            return None

    def find_by_eq(self, field, value):
        if (isinstance(value, numbers.Number)):
            return Paste.objects.raw('Select * FROM pastebin_paste WHERE %s = %d', [field, value])
        else:
            return Paste.objects.raw('Select * FROM pastebin_paste WHERE %s = %s', [field, value])


def paste_to_dto(p: Paste):
    if p is not None:
        json = dict()
        try:
            json['text'] = p.text_field
            json['creation'] = str(p.creation_date)
            json['expiry'] = str(p.expiry_date)
            json['creator'] = p.user.username
            json['expired'] = p.is_expired()
        except Exception:  # Just catch all exceptions as we can return None
            return None
        return json
    else:
        return None


def retrieve_paste(paste_hash):
    retriever = PasteRetriever()
    paste = retriever.get_by_hash(paste_hash)
    return paste
