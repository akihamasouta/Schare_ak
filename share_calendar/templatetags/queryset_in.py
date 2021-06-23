from django import template


register = template.Library()


@register.filter(name="queryset_in")
def queryset_in(value, arg):
    if arg.filter(pk=value.pk):
        TF = True
    else:
        TF = False
    return TF