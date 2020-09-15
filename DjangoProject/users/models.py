from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.contrib.auth import get_user_model
from pathlib import Path

# Create your models here.


class User(AbstractUser):
    username = models.CharField(
        max_length=12,
        unique=True,
        help_text='Required. 12 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    USERNAME_FIELD = 'username'

    class Meta:
        pass


def image_file_path(instance, filename):
    folder = Path('profile_pics')
    user_id = Path(instance.user.username)
    ext = '.jpg'
    return str(folder / user_id.with_suffix(ext))


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to=image_file_path)

    class Meta:
        pass

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
