# -*- coding:utf-8 -*-

import xadmin

from .models import Courses, Lesson, Video, CoursesResource, BannerCourses
from orgnization.models import CourseOrg

class LessonInline(object):
    model = Lesson
    extra = 0


class CoursesResourceInline(object):
    model = CoursesResource
    extra = 0


class CoursesAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degress', 'learn_times', 'students', 'fav_nums', 'get_zj_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degress', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degress', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    list_editable = ['desc', 'degress']
    inlines = [LessonInline, CoursesResourceInline]
    style_fields = {'detail':'ueditor'}
    import_excel = True

    def queryset(self):
        qs = super(CoursesAdmin, self).queryset()
        qs = qs.filter(is_banner = False)
        return qs

    def save_models(self):
        # 保存课程时统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj is not None:
            course_org = obj.course_org
            course_org.course_nums = Courses.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self,request,*args,**kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CoursesAdmin, self).post(request,args,kwargs)


class BannerCoursesAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degress', 'learn_times', 'students', 'fav_nums', 'get_zj_nums','go_to','image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degress', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degress', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    inlines = [LessonInline, CoursesResourceInline]
    style_fields = {'detail': 'ueditor'}

    def queryset(self):
        qs = super(BannerCoursesAdmin, self).queryset()
        qs = qs.filter(is_banner = True)
        return qs

    def save_models(self):
        # 保存课程时统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj is not None:
            course_org = obj.course_org
            course_org.course_nums = Courses.objects.filter(course_org=course_org).count()
            course_org.save()


class LessonAdmin(object):
    list_display = ['courses', 'name', 'add_time']
    search_fields = ['courses__name', 'name']
    list_filter = ['courses', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson__name', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CoursesResourceAdmin(object):
    list_display = ['courses', 'name', 'add_time', 'download']
    search_fields = ['courses__name', 'name', 'download']
    list_filter = ['courses', 'name', 'add_time', 'download']


xadmin.site.register(Courses, CoursesAdmin)
xadmin.site.register(BannerCourses, BannerCoursesAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CoursesResource, CoursesResourceAdmin)

