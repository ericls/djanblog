# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import post, tag


def feed(request):
    posts = post.objects.hidden(hidden=False).all()
    updated = post.objects.latest('pub_date').pub_date
    return render_to_response('feed.xml', {'posts': posts, 'updated': updated})


def archive(request):
    posts = post.objects.filter(hidden=False).all()
    return render_to_response('archive.html', {'posts': posts, 'title':'Archive'})


class index_view(ListView):
    model = post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self, **kwargs):
        return post.objects.filter(hidden=False).all()

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        title = ''
        context['title'] = title
        return context


class tag_view(ListView):
    model = post
    template_name = 'tag.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self, **kwargs):
        t = tag.objects.get(name=self.kwargs.get('slug'))
        return post.objects.filter(tag=t, hidden=False).all()

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        title = self.kwargs.get('slug')
        context['tag'] = tag.objects.get(name=title)
        context['title'] = title
        return context


class post_view(DetailView):
    model = post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        current = context['post']
        current.click += 1
        current.save()

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
