from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='user_images/', blank=True, null=True, default='default_img/user_default.png')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username