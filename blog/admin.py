from django.contrib import admin
from blog.models import post, tag

# Register your models here.

admin.site.register(post)
admin.site.register(tag)
