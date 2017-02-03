

class GoogleUrlShortener:
    def __init__(self):
        from pyshorteners import Shortener
        import logging
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.___shortener = Shortener('Google', api_key=apikey())

    def create_shortened_url(self, url):
        self.logger.info("Called url shortening for: {}".format(url))
        return self.___shortener.short(url) # TODO exception handling and logging

# TODO Centralize
def apikey():
    from common.configurator import Configurator
    c = Configurator()
    return c.conf['googleUrlShortener']['apiKey']
