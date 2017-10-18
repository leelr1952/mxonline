# -*- coding:utf-8 -*-

import xadmin


from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa-fw fa fa-circle-o'


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'image', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'image', 'city__name']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'image', 'city', 'add_time']
    ordering = ['-click_nums']
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'image', 'courseorg', 'add_time']
    search_fields = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'image', 'courseorg__name']
    list_filter = ['name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums', 'image', 'courseorg', 'add_time']
    model_icon = 'fa fa-anchor'


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
