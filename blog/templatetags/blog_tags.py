from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def disqus_shortname():
    return getattr(settings, 'DISQUS_SHORTNAME', "")


@register.simple_tag
def change_page(request, page=1):
    rm = request.resolver_match
    kwargs = rm.kwargs.copy()
    if page == 1:
        kwargs.pop('page', None)
    else:
        kwargs.update({'page': page})
    return reverse(
        rm.url_name,
        args=rm.args,
        kwargs=kwargs
    )
