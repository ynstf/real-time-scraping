from django import template

register = template.Library()

@register.filter
def replace_char(value, args):
    old, new = args.split(',')
    return value.replace(old, new)

