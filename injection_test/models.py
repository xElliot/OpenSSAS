from django.db import models
from .tools import *
# Create your models here.


'''
定义一次扫描任务，model
任务名称
任务注释
任务域名
'''
class Task(models.Model):
    name = models.CharField(max_length=32)
    comment = models.CharField(max_length=100, blank=True)
    page = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


'''
定义一种扫描方式，policy
任务多对多连接
方法名
方法注释
add_url是页面渲染标志
'''
class Policy(models.Model):
    task = models.ManyToManyField(Task, related_name='policies', blank=True)
    name = models.CharField(max_length=32)
    comment = models.CharField(max_length=100, blank=True)
    add_url = models.CharField(max_length=10, default='x')

    def __str__(self):
        return self.name


# 1-get 2-post
'''
定义一个注入点，iobject
任务外键
注入url
注入方法
'''

class IObject(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='i_objects')
    i_url = models.CharField(max_length=32)
    i_method = models.IntegerField(default=1)
    add_url = models.CharField(max_length=10, default='x')

    def __str__(self):
        return get_home(self.i_url)

'''
定义注入点的参数，iparameter
注入点外键
参数名
参数值
'''
class IParameter(models.Model):
    i_object = models.ForeignKey(IObject, on_delete=models.CASCADE, related_name='i_parameters')
    name = models.CharField(max_length=32)
    i_value = models.CharField(max_length=32)

    def __str__(self):
        return self.name


