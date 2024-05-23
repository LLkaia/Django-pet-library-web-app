from django import template


register = template.Library()


@register.filter(name="format_email")
def format_email(value):
    return "<" + value.split("@")[0] + ">"
