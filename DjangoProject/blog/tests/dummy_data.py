import string
import random

from blog.models import Post
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
