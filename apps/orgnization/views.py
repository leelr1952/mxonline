# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from orgnization.models import CityDict, CourseOrg, Teacher
from orgnization.forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Courses

import json
# Create your views here.


class OrgView(View):

    def get(self, request):
        all_org = CourseOrg.objects.all()
        hot_orgs = all_org.order_by("-click_nums")[:5]
        all_city = CityDict.objects.all()

        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_org = CourseOrg.objects.filter(Q(name__icontains=search_keywords) |
                                                 Q(desc__icontains=search_keywords))

        city_id = request.GET.get('city', '')

        if city_id:
            all_org = all_org.filter(city_id = int(city_id))

        category = request.GET.get('ct', '')

        if category:
            all_org = all_org.filter(category=category)

        sort = request.GET.get("sort", '')

        if sort:
            if sort == 'students':
                all_org = all_org.order_by("-students")
            elif sort == 'courses':
                all_org = all_org.order_by("-course_nums")

        org_nums = all_org.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_org, 5, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            "all_org":orgs,
            "all_city":all_city,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort
        })


class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            res = {}
            res['status'] = 'success'
            # return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            res = {}
            res['status'] = 'fail'
            res['msg'] = '添加出错'
            # return HttpResponse("{'status':'fail'}, {'msg':'添加出错'}", content_type='application/json')
        return HttpResponse(json.dumps(res), content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.courses_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:3]
        return render(request, 'org-detail-homepage.html', {
            "all_courses":all_courses,
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page,
            "has_fav":has_fav,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.courses_set.all()
        return render(request, 'org-detail-course.html', {
            "all_courses":all_courses,
            "course_org":course_org,
            "current_page":current_page,
            "has_fav":has_fav
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            "course_org":course_org,
            "current_page":current_page,
            "has_fav":has_fav
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))

        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page,
            "has_fav":has_fav
        })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get("fav_id", 0)
        fav_type = request.POST.get("fav_type", 0)

        res = {}
        if not request.user.is_authenticated():
            res['status'] = 'fail'
            res['msg'] = u'用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        if exist_records:
            exist_records.delete()

            if int(fav_type) == 1:
                course = Courses.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()

            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()

            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            res['status'] = 'fail'
            res['msg'] = u'收藏'
            return HttpResponse(json.dumps(res), content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Courses.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()

                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()

                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                res['status'] = 'success'
                res['msg'] = u'已收藏'
                return HttpResponse(json.dumps(res), content_type='application/json')

            else:
                res['status'] = 'fail'
                res['msg'] = u'收藏出错'
                return HttpResponse(json.dumps(res), content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        sorted_teachers = all_teachers.order_by("-click_nums")[:3]

        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teachers = Teacher.objects.filter(Q(name__icontains=search_keywords) |
                                                  Q(work_company__icontains=search_keywords)|
                                                  Q(work_position__icontains=search_keywords))

        sort = request.GET.get("sort", '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by("-click_nums")

        teacher_nums = all_teachers.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)
        return render(request, 'teachers-list.html',{
            "all_teachers":teachers,
            "teacher_nums":teacher_nums,
            "sort":sort,
            "sorted_teachers":sorted_teachers,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        courses = Courses.objects.filter(teacher=teacher)

        has_teacher_favd = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                has_teacher_favd = True

        has_org_favd = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.courseorg.id):
                has_org_favd = True

        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        return render(request, 'teacher-detail.html', {
            "teacher":teacher,
            "courses":courses,
            "souted_teachers":sorted_teachers,
            "has_teacher_favd":has_teacher_favd,
            "has_org_favd":has_org_favd,
        })