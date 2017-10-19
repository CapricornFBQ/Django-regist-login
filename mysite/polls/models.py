from django.db import models
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.
from django.db import models
import datetime
from django.utils import timezone


# 创建用户对象
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    #在已存在的类中添加新的字段，需要设置默认值
    email = models.EmailField(default="example@qq.com")
    #此处在python3中必须使用str方法 在python2中使用unicode方法
    def __str__(self):
        return self.username


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <=now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Pbulished recently'

class Choice(models.Model):
    # 变量名在字表中对应的是字段
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
