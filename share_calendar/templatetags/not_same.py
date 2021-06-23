from django import template


register = template.Library()


@register.filter(name="not_same")
def not_same(value, arg):
    if value.filter(schedule=arg):
        TF = True
    else:
        TF = False
    return TF