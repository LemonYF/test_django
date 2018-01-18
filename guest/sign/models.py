from django.db import models


# Create your models here.
# 发布会表
class Event(models.Model):
    name = models.CharField(max_length=100)
    limit = models.IntegerField()
    status = models.BooleanField()
    address = models.CharField(max_length=200)
    start_time = models.DateTimeField('events time')  # 发布会时间
    create_time = models.DateTimeField(auto_now=True)  # 创建时间，为当前时间

    def __str__(self):
        return self.name  # 告诉Python如何将对象以str的形式显示出来


# 嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event)  # 关联发布会id
    realname = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    sign = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:  # 内部类定义模型类的行为特性
        unique_together = ("event", "phone")  # 设置两个字段为联合主键

    def __str__(self):
        return self.realname
