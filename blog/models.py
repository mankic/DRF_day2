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
    start_view = models.DateField('노출시작', null=True)
    end_view = models.DateField('노출종료', null=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.ForeignKey(User, verbose_name='작성자', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name='게시글', on_delete=models.CASCADE)
    content = models.TextField('본문')

    def __str__(self):
        return self.content