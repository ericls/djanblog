from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def disqus_shortname():
    return getattr(settings, 'DISQUS_SHORTNAME', "")
