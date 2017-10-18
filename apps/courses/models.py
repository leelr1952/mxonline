# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from orgnization.models import CourseOrg, Teacher

# Create your models here.


class Courses(models.Model):
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, verbose_name=u'课程机构')
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'课程详情',width=600, height=300, imagePath="courses/ueditor/", filePath="courses/ueditor/",
             default='')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    degress = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')),max_length=2,verbose_name=u'课程难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
    image = models.ImageField(upload_to="courses/%Y/%m",verbose_name=u'封面图片')
    click_nums = models.IntegerField(default=0,verbose_name=u'点击人数')
    category = models.CharField(default=u'后端开发', max_length=50, verbose_name=u'课程类别')
    tag = models.CharField(default='', max_length=15, verbose_name=u'课程标签')
    youneed_know = models.CharField(default='', max_length=300, verbose_name=u'课程须知')
    teacher_tell = models.CharField(default='', max_length=300, verbose_name=u'老师告诉')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()
    get_zj_nums.short_description = u'章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.qq.com'>跳转</a>")
    go_to.short_description = u'跳转'

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()

    def __unicode__(self):
        return self.name


class BannerCourses(Courses):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    courses = models.ForeignKey(Courses, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        return self.video_set.all()

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.CharField(max_length=200, verbose_name=u'访问地址', default="")
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟数）')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CoursesResource(models.Model):
    courses = models.ForeignKey(Courses, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    download = models.FileField(upload_to="courses/resource/%Y/%m", verbose_name=u'资源文件',max_length=100)

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
