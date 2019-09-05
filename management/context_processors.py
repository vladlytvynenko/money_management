from django.conf import settings
import datetime


def get_settings(request):
    return {
        'CURRENCY': settings.CURRENCY,
        'TODAY': datetime.datetime.now(),
        'TODAY_STRING': datetime.datetime.now().strftime("%d %B %Y"),
    }
