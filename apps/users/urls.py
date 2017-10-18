# -*-coding:utf-8-*-
from django.conf.urls import url,include

from users.views import UserInfoView, UploadImageView, \
    UpdatePwdView, SendEmailCodeView, UpdateEmailView, \
    MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MymessageView

urlpatterns = [

    url(r'^info/$', UserInfoView.as_view(), name='user_info'),

    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),

    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),

    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    #我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),

    #我收藏的机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),

    #我收藏的教师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),

    #我收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),

    #我的消息
    url(r'^mymessage/$', MymessageView.as_view(), name='mymessage'),

]