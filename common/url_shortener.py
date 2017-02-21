# TODO Maybe salvage own REST api client from the pyshortener source, as this is quite buggy
class GoogleUrlShortener:
    def __init__(self):
        from pyshorteners import Shortener
        import logging
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.shortener = Shortener('Google', api_key=apikey())

    def create_shortened_url(self, url):
        self.logger.info("Called url shortening for: {}".format(url))
        try:
            shortened_url = self.shortener.short(url)
            return shortened_url
        except Exception as e:
            self.logger.exception("Shortening url caused exception: {}".format(e))
            return None

    def create_shortened_url_json(self, url):
        json = {}
        s_u = self.create_shortened_url(url)
        if s_u is not None:
            json["shortened_url"] = s_u
            return json
        else:
            return None

# TODO Centralize
def apikey():
    from common.configurator import Configurator
    c = Configurator()
    return c.conf['google_url_shortener']['api_key']
