from django.test import TestCase
from django.urls import reverse
from .dummy_data import GenerateData


class PostListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_posts = 15
        dummy_data = GenerateData()

        for _ in range(number_of_posts):
            dummy_data.createTestPost()

    def testViewUrlExists(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def testViewUrlAccessible(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)

    def testViewTemplateUsed(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def testPagination(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['posts']), 6)

    def testRemainingPosts(self):
        response = self.client.get(reverse('blog-home')+'?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['posts']), 3)
