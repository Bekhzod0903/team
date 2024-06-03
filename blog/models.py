from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import CustomUser

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name



class Post(models.Model):
    image = models.ImageField(upload_to='media/images')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'posts'

    def __str__(self):
        return self.title



class Review(models.Model):
    comment = models.CharField(max_length=200)
    star_given = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
     )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table ='review'

    def __str__(self):
        return f'{self.star_given} - {self.post.title} - {self.user.username}'
    