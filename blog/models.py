from unicodedata import category
from django.db import models
from user.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField('카테고리', max_length=20)
    desc = models.TextField('내용')

    def __str__(self):
        return self.name

class Article(models.Model):
    category = models.ManyToManyField(Category, verbose_name='카테고리')
    author = models.ForeignKey(User, verbose_name='작성자', on_delete=models.SET_NULL, null=True)
    title = models.CharField('제목', max_length=20)
    content = models.TextField('내용')
    
    def __str__(self):
        return self.title