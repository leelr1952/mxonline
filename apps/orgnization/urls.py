# -*- coding:utf-8 -*-
from django.conf.urls import url,include

from orgnization.views import OrgView, UserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView, TeacherListView, TeacherDetailView


urlpatterns = [

    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', UserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),

    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),

]

#全局404配置
handler404 = 'users.views.page_not_found'
#全局500配置
handler500 = 'users.views.page_error'