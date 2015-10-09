from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
import mistune


class Post(models.Model):
    title = models.CharField(max_length=500, unique=True)
    slug = models.SlugField()
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField('pub_date', auto_now_add=True)
    update_time = models.DateTimeField('update time', auto_now=True)
    tag = models.ManyToManyField('Tag', blank=True)
    content_raw = models.TextField()
    content = models.TextField(default='', null=True, blank=True)
    click = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)
    order = models.IntegerField(default=10)

    class Meta:
        ordering = ['-pub_date']

    def increase_click(self):
        Post.objects.filter(id=self.id).update(click=F('click') + 1)

    def save(self, *args, **kwargs):
        self.content = mistune.markdown(self.content_raw)
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name
