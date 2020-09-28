import string
import random

from django.test import TestCase
from blog.models import Post, Comment, Like
from django.contrib.auth import get_user_model


class GenerateData:

    def __init__(self, seed=0):
        """
        sets the seed for generating the random data.
        """
        random.seed(seed)

    @staticmethod
    def getRandomString(length):
        """
        returns string of random alphabets.
        """
        letters = string.ascii_letters
        res = ''.join(random.choice(letters) for _ in range(length))
        return res

    def createTestUser(self):
        """
        creates a dummy user for testing.
        """
        username = self.getRandomString(6)
        email = f'{username}@django.app'
        password = self.getRandomString(12)
        user = get_user_model().objects.create_user(username=username,
                                                    email=email,
                                                    password=password)
        return user

    def createTestPost(self, title='Hello, World!'):
        """
        creates a dummy post for testing.
        """
        author = self.createTestUser()
        if author is None:
            raise TypeError('User Model object was not created.')

        content = self.getRandomString(100)
        post = Post.objects.create(title=title,
                                   content=content,
                                   author=author)
        return post


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        gets dummy post from GenerateData.
        """
        dummyData = GenerateData()
        post = dummyData.createTestPost()
        if post is None:
            raise TypeError('Post Model object was not created.')

    def testTitleMaxLength(self):
        """
        tests if the post title is limited to a certain length.
        """
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def testDatePostedAutoNowAdd(self):
        """
        tests if the date field is set to automatically reflect the current date.
        """
        post = Post.objects.get(id=1)
        auto_now_add = post._meta.get_field('date_posted').auto_now_add
        self.assertTrue(auto_now_add)

    def testAuthorLabel(self):
        """
        tests whether the post author label is as expected.
        """
        post = Post.objects.get(id=1)
        title = post._meta.get_field('author').verbose_name
        self.assertEquals(title, 'author')

    def testViewCountDefault(self):
        """
        tests if the post view count starts from 0 when a new post is created.
        """
        post = Post.objects.get(id=1)
        view_count = post._meta.get_field('view_count').default
        self.assertEquals(view_count, 0)

    def testObjectName(self):
        """
        tests for the string representation of the object.
        """
        post = Post.objects.get(id=1)
        self.assertEquals(str(post), 'Hello, World!')

    def testGetAbsoluteUrl(self):
        """
        tests for the URL returned by the specific object.
        """
        post = Post.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(), '/post/1/')


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        gets dummy post and comment author from GenerateData.
        """
        dummyData = GenerateData()
        post = dummyData.createTestPost()
        if post is None:
            raise TypeError('Post Model object was not created.')

        author = dummyData.createTestUser()
        if author is None:
            raise TypeError('User Model object was not created.')

        Comment.objects.create(post=post, author=author,
                               content='This is a test comment on a user post.')

    def testContentMaxLength(self):
        """
        tests if the comment is limited to a certain length.
        """
        comment = Comment.objects.select_related('post').get(id=1)
        max_length = comment._meta.get_field('content').max_length
        self.assertEquals(max_length, 256)

    def testDatePosted(self):
        """
        tests if the date field is set to automatically reflect the current date.
        """
        comment = Comment.objects.select_related('post').get(id=1)
        auto_now_add = comment._meta.get_field('date_posted').auto_now_add
        self.assertTrue(auto_now_add)


class LikeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        gets dummy post and like user from GenerateData.
        """
        dummyData = GenerateData()
        post = dummyData.createTestPost()
        if post is None:
            raise TypeError('Post Model object was not created.')

        user = dummyData.createTestUser()
        if user is None:
            raise TypeError('User Model object was not created.')

        Like.objects.create(post=post, user=user)

    def testDateCreated(self):
        """
        tests if the date field is set to automatically reflect the current date.
        """
        like = Like.objects.select_related('post').get(id=1)
        auto_now_add = like._meta.get_field('created').auto_now_add
        self.assertTrue(auto_now_add)
