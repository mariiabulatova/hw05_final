import datetime as dt


def year(request):
    """Добавляет переменную с текущим годом."""
    now = dt.datetime.today()
    year = int(now.strftime('%Y'))
    return {
        'year': year
    }
