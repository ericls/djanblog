from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from blog.models import Post, Tag
from selenium import webdriver
import random


class BlogViewerTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        author = User.objects.create_user(
            username="user1", email="test1@example.com", password="pwd1"
        )
        self.tags = [
            Tag.objects.create(name='tag_%s' % i) for i in range(10)
        ]
        for i in range(10):
            p = Post.objects.create(
                title='Post %s' % i,
                author=author,
                content_raw="Post *1*",
            )
            p.tag.add(random.choice(self.tags))

    def tearDown(self):
        self.browser.quit()

    def test_hidden_posts(self):
        post = Post.objects.latest('pub_date')

        self.browser.get(self.live_server_url+reverse('index'))
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(post.title, body.text)

        self.browser.get(self.live_server_url+reverse('archive'))
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(post.title, body.text)

        self.browser.get(self.live_server_url+reverse(
            'tag', kwargs={'slug': post.tag.first().name}
        ))
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(post.title, body.text)

        post.hidden = True
        post.save()

        self.browser.get(self.live_server_url+reverse('index'))
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn(post.title, body.text)

        self.browser.get(self.live_server_url+reverse('archive'))
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn(post.title, body.text)

        self.browser.get(self.live_server_url+reverse(
            'tag', kwargs={'slug': post.tag.first().name}
        ))
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn(post.title, body.text)

    def test_index(self):
        self.browser.get(self.live_server_url+reverse('index'))
        body = self.browser.find_element_by_tag_name('body')
        for post in Post.objects.all()[:3]:
            self.assertIn(post.title, body.text)

    def test_tag(self):
        tag = random.choice(Tag.objects.all())
        self.browser.get(self.live_server_url+reverse(
            'tag', kwargs={'slug': tag.name}
        ))
        body = self.browser.find_element_by_tag_name('body')
        for post in Post.objects.filter(tag__name=tag.name)[:3]:
            self.assertIn(post.title, body.text)

    def test_archive(self):
        self.browser.get(self.live_server_url+reverse('archive'))
        body = self.browser.find_element_by_tag_name('body')
        for post in Post.objects.all()[:3]:
            self.assertIn(post.title, body.text)

    def test_post(self):
        # Show a post with corrent content and next, prev
        pass

    def test_pagination(self):
        pass

    def test_unauthorized_page(self):
        pass
