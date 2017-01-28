from enum import Enum
from datetime import datetime,timedelta
from pastebin.models import Duration

class PasteDates:
    def __init__(self):
        super().__init__()
    def current_date(self):
        return datetime.now()
    def expiration_date(self, d: Duration):
        return add_to_date(self.current_date(), d)
    def resolve(self, s):
        d = Duration.FifteenMinutes
        try:
            d = Duration[s]
        except Exception:
            pass
        return d

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