from enum import Enum
from django.utils import timezone as datetime
from datetime import timedelta
from pastebin.models import Duration, Paste

class PasteDates:
    def __init__(self):
        super().__init__()

    def is_expired(self, paste:Paste):
        now = self.now()
        expiry = add_to_date(paste.creation_date, paste.expiration)
        if(now > expiry):
            return True
        else:
            return False

    def now(self):
        return datetime.now()

    def create_expiration_date(self, d: Duration):
        return add_to_date(self.now(), d)

    def resolve(self, s):
        d = Duration.FifteenMinutes
        try:
            d = Duration[s]
        except Exception:
            pass
        return d

    def get_expiration_date(self, datetime:datetime, duration:Duration):
        return add_to_date(datetime, duration)

def add_day():
    return datetime.now() + timedelta(days=1)

def add_week():
    return datetime.now() + timedelta(week=1)

def add_fifteenminutes():
    return  datetime.now() + timedelta(minutes=15)

def add_year():
    return  datetime.now() + timedelta(year=1)

def add_month():
    return  datetime.now() + timedelta(month=1)

def add_duration(d:Duration):
    switch = {
        Duration.Year: add_year(),
        Duration.Month: add_month(),
        Duration.Week: add_week(),
        Duration.Day: add_day(),
        Duration.FifteenMinutes: add_fifteenminutes()
    }
    return switch[d]


def add_to_date(dt:datetime, dur:Duration):
    return dt + timedelta(minutes=dur.addition_minutes)