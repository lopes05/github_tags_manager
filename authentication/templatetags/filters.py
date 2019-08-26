from django import template

register = template.Library()

@register.filter
def build_tags(lista):
    return ','.join(lista['names'])