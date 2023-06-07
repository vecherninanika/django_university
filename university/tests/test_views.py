from django.test import TestCase
from university_app.models import Faculty, Group, Teacher, Lesson, Mark, Hometask
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from django.contrib.auth.models import User
from django.test.client import Client
from string import ascii_lowercase
from university_app.config import PAGINATE_THRESHOLD
from university_app import config
from . import attrs
from django.db.models import Model


def create_view_tests(url: str, page_name: str, template: str, cls_model: Model, object_attrs: dict):
    class ViewTests(TestCase):

        def setUp(self):
            self.client = Client()
            some_string = ascii_lowercase[:10]
            self.user = User.objects.create_user(
                username=some_string, password=some_string)
            self.client.login(username=some_string, password=some_string)
            new_fields = attrs.set_up(cls_model)
            for field, value in new_fields.items():
                object_attrs[field] = value
            cls_model.objects.create(**object_attrs)

        def test_view_exists_at_url(self):
            self.assertEqual(self.client.get(url).status_code, HTTP_200_OK)

        def test_view_exists_by_name(self):
            self.assertEqual(self.client.get(
                reverse(page_name)).status_code, HTTP_200_OK)

        def test_view_uses_template(self):
            resp = self.client.get(reverse(page_name))
            self.assertEqual(resp.status_code, HTTP_200_OK)
            self.assertTemplateUsed(resp, template)

        def test_pagination(self):
            pagination_key = 'is_paginated'
            resp_get = self.client.get(reverse(page_name))
            self.assertEqual(resp_get.status_code, HTTP_200_OK)
            self.assertTrue(pagination_key in resp_get.context)
            if resp_get.context.get(pagination_key):
                fst_page = self.client.get(
                    reverse(page_name), {'query': '', 'page': 1})
                self.assertEqual(len(fst_page.context.get(
                    f'{page_name}_list')), PAGINATE_THRESHOLD)
                snd_page = self.client.get(
                    reverse(page_name), {'query': '', 'page': 2})
                self.assertEqual(
                    len(snd_page.context.get(f'{page_name}_list')), 1)

    return ViewTests


FacultyViewTests = create_view_tests(
    '/faculties/', 'faculties', config.FACULTIES_CATALOG, Faculty, attrs.faculty_attrs)
GroupViewTests = create_view_tests(
    '/groups/', 'groups', config.GROUPS_CATALOG, Group, attrs.group_attrs)
TeacherViewTests = create_view_tests(
    '/teachers/', 'teachers', config.TEACHERS_CATALOG, Teacher, attrs.teacher_attrs)
LessonViewTests = create_view_tests(
    '/lessons/', 'lessons', config.LESSONS_CATALOG, Lesson, attrs.lesson_attrs)
MarkViewTests = create_view_tests(
    '/marks/', 'marks', config.MARKS_CATALOG, Mark, attrs.mark_attrs)
HometaskViewTests = create_view_tests(
    '/hometasks/', 'hometasks', config.HOMETASKS_CATALOG, Hometask, attrs.hometask_attrs)
