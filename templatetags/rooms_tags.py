from pickle import TRUE
from django import template

# from rooms import Post

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    pass
