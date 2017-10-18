# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import json


from users.models import UserProfile, EmailVerifyRecord, Banner
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse,UserFavorite, UserMessage
from orgnization.models import CourseOrg, Teacher
from courses.models import Courses

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg":u'用户已经存在'})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()

            #写入注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册慕学网，哈哈"
            user_message.save()

            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)

            if user is not None:
                if user.is_active:

                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "login.html", {"msg": u'用户未激活'})
            else:
                return render(request, "login.html", {"msg": u'用戶名或密碼錯誤'})

        else:
            return render(request, "login.html", {"login_form": login_form})


class ForgetPwdView(View):
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forgetpwd_form":forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")

        else:
            return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {"email":email})

        else:
            return render(request, "active_fail.html")
        # return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            password = request.POST.get("password", "")
            password2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if password == password2:
                user_profile = UserProfile.objects.get(email=email)
                user_profile.password = make_password(password)
                user_profile.save()
                return render(request, "login.html")

            else:
                return render(request, 'password_reset.html', {"email": email, "msg":u'密码不一致'})

        else:
            email = request.POST.get("email", "")
            return render(request, 'password_reset.html', {"email": email, "modifypwd_form":modifypwd_form})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'myself'
        return render(request, "usercenter-info.html", {
            'current_page':current_page
        })

    def post(self, request):
        res = {}
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            res['status'] = 'success'
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')

class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        res = {}
        upload_image = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if upload_image.is_valid():
            upload_image.save()
            res['status'] = 'success'
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            res['status'] = 'fail'
            return HttpResponse(json.dumps(res), content_type='application/json')


class UpdatePwdView(View):
    def post(self, request):
        res = {}
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password", "")
            pwd2 = request.POST.get("password2", "")

            if pwd1 != pwd2:
                res['status'] = 'fail'
                res['msg'] = '密码不一致'
                return HttpResponse(json.dumps(res), content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            res['status'] = 'success'

        else:
            res = modify_form.errors
        return HttpResponse(json.dumps(res), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self,request):
        res={}
        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            res['email'] = '邮箱已存在'
            return HttpResponse(json.dumps(res), content_type='application/json')

        else:
            send_register_email(email, "update")
            res['status'] = 'success'
            return HttpResponse(json.dumps(res), content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        res = {}

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            res['status'] = 'success'
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            res['email'] = '验证码错误'
            return HttpResponse(json.dumps(res), content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    '''
    我的课程
    '''
    def get(self, request):
        current_page = 'course'
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses':user_courses,
            'current_page':current_page,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    '''
    我收藏的机构
    '''
    def get(self, request):
        current_page = 'collection'
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list':org_list,
            'current_page':current_page,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    '''
    我收藏的教师
    '''
    def get(self, request):
        current_page = 'collection'
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list':teacher_list,
            'current_page':current_page,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    '''
    我收藏的课程
    '''
    def get(self, request):
        current_page = 'collection'
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course = Courses.objects.get(id=fav_course.fav_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list':course_list,
            'current_page':current_page,
        })


class MymessageView(LoginRequiredMixin, View):
    '''
    我的消息
    '''
    def get(self, request):
        current_page = 'message'
        all_messages = UserMessage.objects.filter(user=request.user.id)
        uuu = request.user.get_unread_nums()

        all_unread_messages = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'messages':messages,
            'current_page':current_page,
        })


class IndexView(View):
    #慕学在线首页
    def get(self, request):
        #print 1/0 出现500错误
        all_banners = Banner.objects.all().order_by('index')
        courses = Courses.objects.filter(is_banner=False)[:6]
        banner_courses = Courses.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs

        })


def page_not_found(request):
    #全局404配置页面
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response


def page_error(request):
    #全局500配置页面
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response