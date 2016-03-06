from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'djanblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^panel-eric/', include(admin.site.urls)),
    url(r'', include('blog.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
