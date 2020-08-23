from django.db import models
# from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from markdown_deux import markdown
from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed
from django.contrib.auth import get_user_model

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)

    contentHelpText = markdown_allowed() + " <a id='ref'>Quick reference</a>"
    content = models.TextField(help_text=contentHelpText)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    view_count = models.PositiveIntegerField(default=0)

    tags = TaggableManager()
    TAGGIT_CASE_INSENSITIVE = True


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
        

    def getContent(self):
        return markdown(self.content)