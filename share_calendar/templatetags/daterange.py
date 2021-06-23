from django import template
from datetime import timedelta


register = template.Library()


@register.filter(name="daterange", expects_localtime=True)
def daterange(value, arg):
    date_list = []
    for n in range((arg - value).days):
        date_list.append(value + timedelta(n))
    return date_list[1::]
