from django.test import TestCase
from blog.models import Post, Comment, Like
from django.contrib.auth import get_user_model


def createTestAuthor(username, email, password):
    return get_user_model().objects.create_user(username=username,
                                                email=email,
                                                password=password)


def createTestPost(username, email, password, title='Hello, World!', content='Hello, this is the content for my test case.'):
    author = createTestAuthor(
        username=username, email=email, password=password)
    if author is None:
        raise TypeError('User Model object was not created.')

    return Post.objects.create(title=title,
                               content=content,
                               author=author)


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        post = createTestPost(
            username='user1', email='user1@django.app', password='testPassword')
        if post is None:
            raise TypeError('Post Model object was not created.')

    def testTitleMaxLength(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def testDatePostedAutoNowAdd(self):
        post = Post.objects.get(id=1)
        auto_now_add = post._meta.get_field('date_posted').auto_now_add
        self.assertTrue(auto_now_add)

    def testAuthorLabel(self):
        post = Post.objects.get(id=1)
        title = post._meta.get_field('author').verbose_name
        self.assertEquals(title, 'author')

    def testViewCountDefault(self):
        post = Post.objects.get(id=1)
        view_count = post._meta.get_field('view_count').default
        self.assertEquals(view_count, 0)

    def testObjectName(self):
        post = Post.objects.get(id=1)
        self.assertEquals(str(post), 'Hello, World!')

    def testGetAbsoluteUrl(self):
        post = Post.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(), '/post/1/')


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        post = createTestPost(
            username='user2', email='user2@django.app', password='testpassword2')
        if post is None:
            raise TypeError('Post Model object was not created.')

        author = createTestAuthor(
            username='user3', email='user3@django.app', password='testpassword3')
        if author is None:
            raise TypeError('User Model object was not created.')

        Comment.objects.create(post=post, author=author,
                               content='This is a test comment on a user post.')

    def testContentMaxLength(self):
        comment = Comment.objects.select_related('post').get(id=1)
        max_length = comment._meta.get_field('content').max_length
        self.assertEquals(max_length, 256)
