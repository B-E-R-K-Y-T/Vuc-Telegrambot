from datetime import date, timedelta


def get_tomorrow_date(days=1):
    today = date.today()
    tomorrow_date = today + timedelta(days=days)

    return tomorrow_date
