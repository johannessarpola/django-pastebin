from django.core.management import BaseCommand

class Command(BaseCommand):
        # This is not used as it's done through django-cron, see cron-folder for the jobs
        def handle(self, *args, **options):
            from pastebin import maintainer
            maintainer.cleanup_db()