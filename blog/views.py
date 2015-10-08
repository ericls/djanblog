# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import Post, Tag


def feed(request):
    posts = Post.objects.filter(hidden=False).all()
    updated = Post.objects.latest('pub_date').pub_date
    return render_to_response('feed.xml', {'posts': posts, 'updated': updated})


def archive(request):
    posts = Post.objects.filter(hidden=False).all()
    return render_to_response('archive.html', {'posts': posts, 'title':'Archive'})


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self, **kwargs):
        return Post.objects.filter(hidden=False).all()

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        title = ''
        context['title'] = title
        return context


class TagView(ListView):
    model = Post
    template_name = 'tag.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self, **kwargs):
        t = Tag.objects.get(name=self.kwargs.get('slug'))
        return Post.objects.filter(tag=t, hidden=False).all()

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        title = self.kwargs.get('slug')
        context['tag'] = Tag.objects.get(name=title)
        context['title'] = title
        return context


class PostView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        current = self.object
        current.increase_click()

        try:
            next_post = current.get_next_by_pub_date()
        except:
            next_post = None

        try:
            previous_post = current.get_previous_by_pub_date()
        except:
            previous_post = None

        context['next'] = next_post
        context['previous'] = previous_post
        context['title'] = current.title

        return context
