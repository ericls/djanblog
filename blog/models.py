from django.db import models
from django.contrib.auth.models import User
import mistune


class post(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField()
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField('pub_date', auto_now_add=True)
    update_time = models.DateTimeField('update time', auto_now=True)
    tag = models.ManyToManyField('tag', null=True, blank=True)
    content_raw = models.TextField()
    content = models.TextField(default='')
    click=models.IntegerField(default=0)
    hidden=models.BooleanField(default=False)
    order = models.IntegerField(default=10)

    class Meta:
        ordering = ['-pub_date']

    def save(self, *args, **kwargs):
        self.content = mistune.markdown(self.content_raw)
        super(post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class tag(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
