from django.conf.urls import patterns, url
from blog.views import IndexView, TagView, PostView, archive, editor, feed

urlpatterns = [
    url(r'^$', IndexView.as_view(), {'page': 1}, name='index'),
    url(r'^feed/$', feed, name='feed'),
    url(r'^archive/$', archive, name='archive'),
    url(r'^post/(?P<slug>.*?)/$', PostView.as_view(), name='post'),
    url(r'^page/(?P<page>\d+)/$', IndexView.as_view(), name='index'),
    url(
        r'^tag/(?P<slug>.*?)/page/(?P<page>\d+)/$',
        TagView.as_view(),
        name='tag'
    ),
    url(r'^tag/(?P<slug>.*?)/$', TagView.as_view(), name='tag'),
    url(r'^new/$', editor, name='new_post'),
    url(r'^edit/(?P<slug>.*?)/$', editor, name='edit_post'),
]
