from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from markdown_deux import markdown
from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed
from django.contrib.auth import get_user_model

# Created the models here.


class Post(models.Model):
    """
    Database model for individual posts.
    """

    title = models.CharField(max_length=100)
    contentHelpText = markdown_allowed() + " <a id='ref'>Quick reference</a>"
    content = models.TextField(help_text=contentHelpText)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)

    tags = TaggableManager()
    TAGGIT_CASE_INSENSITIVE = True

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def getContent(self):
        return markdown(self.content)


class Comment(models.Model):
    """
    Database model for individual Comments.
    Comments have a Many-to-One relationship with the post and user models.
    """

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='author_comments')
    content = models.TextField(max_length=256, verbose_name='comment',
                               help_text='comment should not exceed 256 characters.')
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'Comment {self.content} posted by {self.author}'


class Like(models.Model):
    """
    Database model for individual Likes.
    Likes have a Many-to-One relationship with the post and user models.
    """

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='user_likes')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return f'Liked on {self.created}'
