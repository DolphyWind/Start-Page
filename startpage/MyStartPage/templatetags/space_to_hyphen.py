from django import template

register = template.Library()

@register.filter
def space_to_hyphen(value):
    return value.replace(" ", "-")