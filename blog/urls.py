from django.conf.urls import patterns, url
from blog.views import index_view, tag_view, post_view

urlpatterns = patterns('blog.views',
        url(r'^$', index_view.as_view(), {'page': 1}, name='index_1'),
        url(r'^feed/$', 'feed', name='feed'),
        url(r'^archive/$', 'archive', name='archive'),
        url(r'^post/(?P<slug>.*?)/$', post_view.as_view(), name='post'),
        url(r'^page/(?P<page>\d+)/$', index_view.as_view(), name='index'),
        url(r'^tag/(?P<slug>.*?)/page/(?P<page>\d+)/$', tag_view.as_view(), name='tag'),
        url(r'^tag/(?P<slug>.*?)/$', tag_view.as_view(), name='tag_1'),
)
