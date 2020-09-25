from django.test import TestCase
from blog.models import Post
from django.contrib.auth import get_user_model


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('models are set up!')
        Post.objects.create(title='Hello World!',
                            content='Hello, this is the content for my test case.',
                            author=get_user_model().objects.create_user(username='testUser',
                                                                        email='testing@django.models',
                                                                        password='test123'))

    def test_title_label(self):
        post = Post.objects.get(id=1)
        title = post._meta.get_field('title').verbose_name
        self.assertEquals(title, 'title')
