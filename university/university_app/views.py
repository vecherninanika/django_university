from typing import Any
from .models import Faculty, Group, Teacher, Lesson, Student, Mark, Hometask
from .serializers import *
from rest_framework import viewsets
from django.db import models
from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from . import config
from rest_framework import permissions, viewsets
from django.db import models
from .forms import AddMarkForm
from django.contrib.auth import decorators as auth_decorators


@auth_decorators.login_required
def profile_page(request):
    user = request.user
    user_data = {
        'Username': user.username,
        'First name': user.first_name,
        'Last name': user.last_name,
        'Email': user.email,
    }
    return render(
        request,
        config.TEMPLATE_PROFILE,
        context={
            'user_data': user_data,
        },
    )


def about_page(request):
    return render(
        request,
        config.TEMPLATE_ABOUT,
    )


def contacts_page(request):
    return render(
        request,
        config.TEMPLATE_CONTACTS,
    )


def custom_main(request):
    return render(
        request,
        config.TEMPLATE_MAIN,
        context={
            'faculties': Faculty.objects.all().count(),
            'groups': Group.objects.all().count(),
            'teachers': Teacher.objects.all().count(),
            'students': Student.objects.all().count(),
        },
    )


def student_objects(student: Student, cls_model: models.Model, order_field: str):
    lessons = []
    for lesson in Lesson.objects.all():
        if student.group in lesson.groups.all():
            lessons.append(lesson)
    if cls_model is Group:
        return [student.group,]
    elif cls_model is Lesson:
        return lessons
    elif cls_model is Mark:
        return Mark.objects.filter(student=student).order_by(order_field)
    elif cls_model is Hometask:
        return Hometask.objects.filter(lesson__in=lessons).order_by(order_field)
    return cls_model.objects.order_by(order_field)


def teacher_objects(teacher: Teacher, cls_model: models.Model, order_field: str):
    lessons = Lesson.objects.filter(teacher=teacher).order_by('day')
    if cls_model is Group:
        groups = []
        for group in Group.objects.all():
            for subject in group.subjects.all():
                if subject in teacher.subjects.all():
                    groups.append(group)
        return groups
    elif cls_model is Lesson:
        return lessons
    elif cls_model is Mark:
        return Mark.objects.filter(lesson__in=Lesson.objects.filter(teacher=teacher)).order_by(order_field)
    elif cls_model is Hometask:
        return Hometask.objects.filter(lesson__in=lessons).order_by(order_field)
    return cls_model.objects.order_by(order_field)


def get_objects_for_user(request, cls_model: models.Model, order_field: str):
    user = request.user
    if user.is_superuser:
        return cls_model.objects.order_by(order_field)
    try:
        student = Student.objects.get(user=user)
    except Exception:
        student = None
    if student:
        return student_objects(student, cls_model, order_field)
    try:
        teacher = Teacher.objects.get(user=user)
    except Exception:
        teacher = None
    if teacher:
        return teacher_objects(teacher, cls_model, order_field)
    if cls_model in (Faculty, Teacher):
        return cls_model.objects.order_by(order_field)
    return []


def catalog_view(cls_model: models.Model, order_field: str, page_name: str, template: str):
    class CustomListView(ListView):
        model = cls_model
        template_name = template
        context_object_name = page_name
        paginate_by = config.PAGINATE_THRESHOLD

        def get_context_data(self, **kwargs: Any):
            context = super().get_context_data(**kwargs)
            instances = get_objects_for_user(
                self.request, cls_model, order_field)
            paginator = Paginator(instances, config.PAGINATE_THRESHOLD)
            page = self.request.GET.get('page')
            page_obj = paginator.get_page(page)
            context[f'{page_name}_list'] = page_obj
            return context
    return CustomListView


FacultyListView = catalog_view(
    Faculty, 'title', 'faculties', config.FACULTIES_CATALOG)
TeacherListView = catalog_view(
    Teacher, 'full_name', 'teachers', config.TEACHERS_CATALOG)
GroupListView = catalog_view(Group, 'faculty', 'groups', config.GROUPS_CATALOG)
LessonListView = catalog_view(Lesson, 'day', 'lessons', config.LESSONS_CATALOG)
MarkListView = catalog_view(Mark, 'lesson', 'marks', config.MARKS_CATALOG)
HometaskListView = catalog_view(
    Hometask, 'lesson', 'hometasks', config.HOMETASKS_CATALOG)


def entity_view(cls_model: models.Model, order_field: str, name: str, template: str):
    def view(request):
        target_obj = cls_model.objects.get(id=request.GET.get('id', ''))
        context = {name: target_obj}

        instances = get_objects_for_user(request, cls_model, order_field)
        context[f'user_{cls_model}'.lower()] = target_obj in instances

        try:
            teacher = Teacher.objects.get(user=request.user)
        except Exception:
            teacher = None
        if cls_model is Lesson:
            context['marks'] = Mark.objects.filter(lesson=target_obj)
            if request.user.is_superuser or teacher:
                if request.method == "POST":
                    form = AddMarkForm(target_obj, request.POST)
                    if form.is_valid():
                        form.save()
                else:
                    form = AddMarkForm(target_obj)
                context['form'] = form
                context['lesson'] = target_obj
                context['form_errors'] = form.errors
        return render(request, template, context=context)
    return view


faculty_view = entity_view(Faculty, 'title', 'faculty', config.FACULTY_ENTITY)
group_view = entity_view(Group, 'faculty', 'group', config.GROUP_ENTITY)
teacher_view = entity_view(
    Teacher, 'full_name', 'teacher', config.TEACHER_ENTITY)
lesson_view = entity_view(Lesson, 'day', 'lesson', config.LESSON_ENTITY)
mark_view = entity_view(Mark, 'lesson', 'mark', config.MARK_ENTITY)
hometask_view = entity_view(
    Hometask, 'lesson', 'hometask', config.HOMETASK_ENTITY)


class Permission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in config.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in config.UNSAFE_METHODS:
            try:
                teacher = Teacher.objects.get(user=request.user)
            except Exception:
                teacher = None
            return bool(request.user and (request.user.is_superuser or teacher))
        return False


def query_from_request(request, serializer=None):
    if serializer:
        query = {}
        for attr in serializer.Meta.fields:
            attr_value = request.GET.get(attr, '')
            if attr_value:
                query[attr] = attr_value
        return query
    return request.GET


def create_viewset(cls_model: models.Model, serializer, order_field: str):
    class_name = f"{cls_model.__name__}ViewSet"
    doc = f"API endpoint that allows users to be viewed or edited for {cls_model.__name__}"
    CustomViewSet = type(class_name, (viewsets.ModelViewSet,), {
        "__doc__": doc,
        "serializer_class": serializer,
        "queryset": cls_model.objects.all().order_by(order_field),
        "permission classes": [Permission],
        "get_queryset": lambda self, *args, **kwargs: cls_model.objects.filter(**query_from_request(self.request, serializer)).order_by(order_field)}
    )

    return CustomViewSet


FacultyViewSet = create_viewset(Faculty, FacultySerializer, 'title')
TeacherViewSet = create_viewset(Teacher, TeacherSerializer, 'full_name')
LessonViewSet = create_viewset(Lesson, LessonSerializer, 'day')
MarkViewSet = create_viewset(Mark, MarkSerializer, 'lesson')
HometaskViewSet = create_viewset(Hometask, HometaskSerializer, 'task')
GroupViewSet = create_viewset(Group, GroupSerializer, 'title')
