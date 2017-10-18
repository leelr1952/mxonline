# -*-coding:utf-8-*-

from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Courses, CoursesResource, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from users.utils.mixin_utils import LoginRequiredMixin

import json

# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Courses.objects.all().order_by("-add_time")
        hot_courses = Courses.objects.all().order_by("-click_nums")[:3]

        search_keywords = request.GET.get('keywords',"")
        if search_keywords:
            all_courses = Courses.objects.filter(Q(name__icontains=search_keywords)|
                                                 Q(desc__icontains=search_keywords)|
                                                 Q(detail__icontains=search_keywords))

        sort = request.GET.get("sort", '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by("-students")
            elif sort == 'hot':
                all_courses = all_courses.order_by("-click_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Courses.objects.get(id=int(course_id))

        course.click_nums+=1
        course.save()

        tag = course.tag
        if tag:
            relative_courses = Courses.objects.filter(Q(tag=tag) & ~Q(name=course.name))

        else:
            relative_courses = []

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        return render(request, 'course-detail.html', {
            'course': course,
            'relative_courses': relative_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
        })


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.courses

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()


        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Courses.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CoursesResource.objects.filter(courses=course)

        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': all_resources,
            'related_courses': related_courses,
            'video': video,
        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Courses.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()


        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Courses.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CoursesResource.objects.filter(courses=course)

        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': all_resources,
            'related_courses': related_courses,
        })


class CommentView(View):
    def get(self, request, course_id):
        course = Courses.objects.get(id=int(course_id))
        all_resources = CoursesResource.objects.filter(courses=course)
        all_comments = CourseComments.objects.all()

        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': all_resources,
            'all_comments': all_comments,
        })


class AddCommentView(View):
    def post(self, request):
        res={}
        if not request.user.is_authenticated():
            res['status'] = 'fail'
            res['msg'] = u'用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get("comment", "")
        if course_id > 0 and comment:
            course_comment = CourseComments()
            course = Courses.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comment
            course_comment.user = request.user
            course_comment.save()
            res['status'] = 'success'
            res['msg'] = u'添加成功'
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            res['status'] = 'fail'
            res['msg'] = u'添加失败'
            return HttpResponse(json.dumps(res), content_type='application/json')

