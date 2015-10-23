# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
import datetime

from django.forms import ModelForm






class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):              # __unicode__ on Python 2
        return self.question_text

    def was_published_recently(self):
        #return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now        


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):              # __unicode__ on Python 2
        return self.choice_text
# Create your models here.

#models
class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)







class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length = 200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank = True, null = True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title




###############################  Form ###############################

class HostList(models.Model):
    ip = models.CharField(max_length=20, verbose_name=u'IP地址')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    product = models.CharField(max_length=20, verbose_name=u'产品')
    application = models.CharField(max_length=20, verbose_name=u'应用')
    idc_jg = models.CharField(max_length=10, blank=True, verbose_name=u'机柜编号')
    status = models.CharField(max_length=10, verbose_name=u'使用状态')
    remark = models.TextField(max_length=50, blank=True, verbose_name=u'备注')

    def __unicode__(self):
        return u'%s - %s - %s' %(self.ip, self.hostname, self.application )

    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = u'主机列表'









