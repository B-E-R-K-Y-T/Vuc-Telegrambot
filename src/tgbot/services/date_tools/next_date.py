from datetime import date, timedelta


def get_next_date(days=1):
    today = date.today()
    next_date = today + timedelta(days=days)

    return next_date
