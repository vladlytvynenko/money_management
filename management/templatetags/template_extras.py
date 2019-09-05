from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def price(value):
    return f"{value:.2f} {settings.CURRENCY}"
