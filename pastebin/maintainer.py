import logging

from pastebin.core.paste_remover import PasteRemover


def cleanup_db():
    """
    Has task related to maintaining database
    :return:
    """
    pd = PasteRemover()
    pd.removeExpiredPastes()
    logging.info("Cleaned database")


def report_load():
    # TODO Find a way to report current load etc to somewhere
    logging.info("Created load report")
    return 0


