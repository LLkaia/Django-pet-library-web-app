from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def user_email(context):
    request = context["request"]
    if request.user.is_authenticated:
        return request.user.email
    return ""
