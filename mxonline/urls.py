# -*- coding:utf8 -*-

"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
from apps.users.views import LogoutView,LoginView, RegisterView, ActiveUserView, \
    ForgetPwdView, ResetView, ModifyPwdView, IndexView
import xadmin
from mxonline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # url(r'^org_list/$', OrgView.as_view(), name='org_list'),
    url(r'^org/', include('orgnization.urls', namespace='org')),

    url(r'^course/', include('courses.urls', namespace='course')),
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)/$', serve, {"document_root":MEDIA_ROOT}),

    # url(r'^static/(?P<path>.*)/$', serve, {"document_root":STATIC_ROOT}),
    # 修改xadmin时注释掉，加上时需从settings中import STATIC_ROOT
    # django中settings里debug在False情况下，静态文件不由django托管，即不在staticfiles_dirs中找，
    # staticfiles_dirs失效，一般在第三方服务器中找，这时需要配置STATIC_ROOT；
    # debug在True情况下，静态文件可由django托管，可直接在staticfiles_dirs找
    url(r'^users/', include('users.urls', namespace='users')),

    # ueditor相关url
    url(r'^ueditor/',include('DjangoUeditor.urls' )),

]
