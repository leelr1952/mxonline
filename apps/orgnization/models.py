# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'城市')
    desc = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    category = models.CharField(max_length=20, choices=(('pxjg', u'培训机构'), ('gx', u'高校'), ('gr', u'个人')),
                                verbose_name=u'机构类别', default='pxjg')
    tag = models.CharField(default=u'全国知名',max_length=10, verbose_name=u'机构标签')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    address = models.CharField(max_length=100, verbose_name=u'地址')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'logo')
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'教师名字')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'工作单位')
    work_position = models.CharField(max_length=50, verbose_name=u'工作职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    years = models.IntegerField(default=18, verbose_name=u'年龄')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name=u'头像')
    courseorg = models.ForeignKey(CourseOrg, verbose_name=u'所在机构')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_courses_nums(self):
        return self.courses_set.all().count()
