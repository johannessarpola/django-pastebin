from django.contrib import messages

class Messenger:
    """
    Simpole wrapper for the django messages
    """
    def __init__(self, domain):
        super().__init__()
        self.domain = domain
        import logging
        self.logger = logging.getLogger(__name__)

    def add_info_to_req(self, request, message):
        messages.add_message(request, messages.INFO, message)

    def add_warn_to_req(self, request, message):
        messages.add_message(request, messages.WARNING, message)

    def add_err_to_req(self, request, message):
        messages.add_message(request, messages.ERROR, message)
        self.logger.warning("Err message raised in domain {} with message: {}".format(self.domain, message))
