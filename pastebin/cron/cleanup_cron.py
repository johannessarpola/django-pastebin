from django_cron import CronJobBase, Schedule

class Cleanup(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'pastebin.cleanup'    # a unique code

    def do(self):
        import pastebin.maintainer as mjobs
        mjobs.cleanup_db()