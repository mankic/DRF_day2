from django.db import models
from datetime import datetime

from user.models import User

# Create your models here.
class Product(models.Model):
    author = models.ForeignKey(User, verbose_name='작성자', on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=30)
    thumbnail = models.FileField('썸네일', upload_to='product/')
    desc = models.TextField('설명')
    created = models.DateTimeField('등록일', auto_now_add=True)
    start_view = models.DateTimeField('노출시작일', default=datetime.now())
    end_view = models.DateTimeField('노출종료일', default=datetime.now())


    def __str__(self):
        return self.title