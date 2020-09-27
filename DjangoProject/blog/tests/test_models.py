from django.test import TestCase
from blog.models import Post
from django.contrib.auth import get_user_model


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Post.objects.create(title='Hello, World!',
                            content='Hello, this is the content for my test case.',
                            author=get_user_model().objects.create_user(username='testUser',
                                                                        email='testing@django.models',
                                                                        password='test123'))

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_date_posted_auto_now_add(self):
        post = Post.objects.get(id=1)
        auto_now_add = post._meta.get_field('date_posted').auto_now_add
        self.assertTrue(auto_now_add)

    def test_author_label(self):
        post = Post.objects.get(id=1)
        title = post._meta.get_field('author').verbose_name
        self.assertEquals(title, 'author')

    def test_view_count_default(self):
        post = Post.objects.get(id=1)
        view_count = post._meta.get_field('view_count').default
        self.assertEquals(view_count, 0)

    def test_object_name(self):
        post = Post.objects.get(id=1)
        self.assertEquals(str(post), 'Hello, World!')

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(), '/post/1/')
