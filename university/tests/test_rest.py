from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from university_app.models import Faculty, Group, Subject, Teacher, Lesson, Student, Mark, Hometask
from rest_framework import status
from rest_framework.test import APIClient
import json
from . import attrs
from university_app.serializers import *
from rest_framework.test import APITestCase
from django.db import models
from rest_framework import serializers


def create_viewset_tests(
    url: str,
    cls_model: models.Model,
    cls_serializer: serializers.ModelSerializer,
    request_content: dict,
    to_change: dict,
):
    class ViewSetTests(APITestCase):

        def setUp(self):
            self.user = User.objects.create_user(
                is_superuser=True,
                id=1,
                username='test',
                first_name='test',
                last_name='test',
                email='test@mail.ru',
                password='test'
            )
            token = Token.objects.create(user=self.user)
            self.client = APIClient()
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            self.model = cls_model.objects.create(**request_content)

        def test_create_model(self):
            """POST."""
            response = self.client.post(url, data=request_content)
            serializer = cls_serializer(data=request_content)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_get_model(self):
            """GET."""
            url_to_get = f'{url}{self.model.id}/'
            response = self.client.get(url_to_get)
            serializer = cls_serializer(data=request_content)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_update_model(self):
            """PUT."""
            url_to_update = f'{url}{self.model.id}/'
            response = self.client.put(
                url_to_update,
                data=json.dumps(to_change),
                content_type='application/json'
            )
            serializer = cls_serializer(data=to_change)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_delete_model(self):
            """DELETE."""
            url_to_delete = f'{url}{self.model.id}/'
            response = self.client.delete(url_to_delete)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertFalse(
                cls_model.objects.filter(id=self.model.id).exists()
            )

    return ViewSetTests


FacultyViewSetTests = create_viewset_tests(
    '/rest/faculty/', Faculty, FacultySerializer, attrs.faculty_attrs, attrs.faculty_new_attrs)


class GroupViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            is_superuser=True,
            id=1,
            username='test',
            first_name='test',
            last_name='test',
            email='test@mail.ru',
            password='test'
        )
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.request_data = attrs.group_attrs.copy()
        self.request_data['faculty'] = attrs.faculty_attrs.copy()
        self.model = Group.objects.create(
            faculty=Faculty.objects.create(
                **attrs.faculty_attrs
            ),
            **attrs.group_attrs
        )
        self.to_change = attrs.group_new_attrs

    def test_create_model(self):
        """POST."""
        response = self.client.post(
            '/rest/group/',
            data=json.dumps(self.request_data),
            content_type='application/json'
        )
        serializer = GroupSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_model(self):
        """GET."""
        url_to_get = f'/rest/group/{self.model.id}/'
        response = self.client.get(url_to_get)
        serializer = GroupSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_model(self):
        """PUT."""
        url_to_update = f'/rest/group/{self.model.id}/'
        response = self.client.patch(
            url_to_update,
            data=json.dumps(
                self.to_change,
            ),
            content_type='application/json'
        )
        serializer = GroupSerializer(data=self.to_change, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_model(self):
        """DELETE."""
        url_to_delete = f'/rest/group/{self.model.id}/'
        response = self.client.delete(url_to_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Group.objects.filter(id=self.model.id).exists()
        )


class TeacherViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            is_superuser=True,
            id=1,
            username='test',
            first_name='test',
            last_name='test',
            email='test@mail.ru',
            password='test'
        )
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.request_data = attrs.teacher_attrs.copy()
        self.request_data['faculty'] = attrs.faculty_attrs
        self.model = Teacher.objects.create(
            faculty=Faculty.objects.create(
                **attrs.faculty_attrs
            ),
            **attrs.teacher_attrs,
            user=self.user
        )
        self.to_change = attrs.teacher_new_attrs

    def test_create_model(self):
        """POST."""
        response = self.client.post(
            '/rest/teacher/',
            data=json.dumps(self.request_data),
            content_type='application/json'
        )
        serializer = TeacherSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_model(self):
        """GET."""
        url_to_get = f'/rest/teacher/{self.model.id}/'
        response = self.client.get(url_to_get)
        serializer = TeacherSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_model(self):
        """PUT."""
        url_to_update = f'/rest/teacher/{self.model.id}/'
        response = self.client.patch(
            url_to_update,
            data=json.dumps(
                self.to_change,
            ),
            content_type='application/json'
        )
        serializer = TeacherSerializer(data=self.to_change, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_model(self):
        """DELETE."""
        url_to_delete = f'/rest/teacher/{self.model.id}/'
        response = self.client.delete(url_to_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Teacher.objects.filter(id=self.model.id).exists()
        )


class LessonViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            is_superuser=True,
            id=1,
            username='test',
            first_name='test',
            last_name='test',
            email='test@mail.ru',
            password='test'
        )
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.request_data = attrs.lesson_attrs.copy()
        self.request_data['subject'] = attrs.subject_attrs.copy()
        self.request_data['teacher'] = attrs.teacher_attrs.copy()
        self.request_data['teacher']['faculty'] = attrs.faculty_attrs
        self.model = Lesson.objects.create(
            subject=Subject.objects.create(
                **attrs.subject_attrs
            ),
            teacher=Teacher.objects.create(
                full_name='test',
                faculty=Faculty.objects.create(**attrs.faculty_attrs)
            ),
            **attrs.lesson_attrs,
        )
        self.to_change = attrs.lesson_new_attrs

    def test_create_model(self):
        """POST."""
        response = self.client.post(
            '/rest/lesson/',
            data=json.dumps(self.request_data),
            content_type='application/json'
        )
        serializer = LessonSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_model(self):
        """GET."""
        url_to_get = f'/rest/lesson/{self.model.id}/'
        response = self.client.get(url_to_get)
        serializer = LessonSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_model(self):
        """PUT."""
        url_to_update = f'/rest/lesson/{self.model.id}/'
        response = self.client.patch(
            url_to_update,
            data=json.dumps(
                self.to_change,
            ),
            content_type='application/json'
        )
        serializer = LessonSerializer(data=self.to_change, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_model(self):
        """DELETE."""
        url_to_delete = f'/rest/lesson/{self.model.id}/'
        response = self.client.delete(url_to_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Lesson.objects.filter(id=self.model.id).exists()
        )


class MarkViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            is_superuser=True,
            id=1,
            username='test',
            first_name='test',
            last_name='test',
            email='test@mail.ru',
            password='test'
        )
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.request_data = attrs.mark_attrs.copy()
        self.request_data['lesson'] = attrs.lesson_attrs.copy()
        self.request_data['lesson']['subject'] = attrs.subject_attrs
        self.request_data['lesson']['teacher'] = attrs.teacher_attrs.copy()
        self.request_data['lesson']['teacher']['faculty'] = attrs.faculty_attrs
        self.request_data['student'] = attrs.student_attrs.copy()
        self.request_data['student']['group'] = attrs.group_attrs.copy()
        self.request_data['student']['group']['faculty'] = attrs.faculty_attrs
        self.model = Mark.objects.create(
            lesson=Lesson.objects.create(
                **attrs.lesson_attrs,
                subject=Subject.objects.create(**attrs.subject_attrs),
                teacher=Teacher.objects.create(
                    **attrs.teacher_attrs,
                    faculty=Faculty.objects.create(**attrs.faculty_attrs)
                )
            ),
            student=Student.objects.create(
                **attrs.student_attrs,
                group=Group.objects.create(
                    **attrs.group_attrs,
                    faculty=Faculty.objects.create(**attrs.faculty_attrs))
            ),
            **attrs.mark_attrs,
        )
        self.to_change = attrs.mark_new_attrs

    def test_create_model(self):
        """POST."""
        response = self.client.post(
            '/rest/mark/',
            data=json.dumps(self.request_data),
            content_type='application/json'
        )
        serializer = MarkSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_model(self):
        """GET."""
        url_to_get = f'/rest/mark/{self.model.id}/'
        response = self.client.get(url_to_get)
        serializer = MarkSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_model(self):
        """PUT."""
        url_to_update = f'/rest/mark/{self.model.id}/'
        response = self.client.patch(
            url_to_update,
            data=json.dumps(
                self.to_change,
            ),
            content_type='application/json'
        )
        serializer = MarkSerializer(data=self.to_change, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_model(self):
        """DELETE."""
        url_to_delete = f'/rest/mark/{self.model.id}/'
        response = self.client.delete(url_to_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Mark.objects.filter(id=self.model.id).exists()
        )


class HometaskViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            is_superuser=True,
            id=1,
            username='test',
            first_name='test',
            last_name='test',
            email='test@mail.ru',
            password='test'
        )
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.request_data = attrs.hometask_attrs.copy()
        self.request_data['lesson'] = attrs.lesson_attrs.copy()
        self.request_data['lesson']['subject'] = attrs.subject_attrs
        self.request_data['lesson']['teacher'] = attrs.teacher_attrs.copy()
        self.request_data['lesson']['teacher']['faculty'] = attrs.faculty_attrs
        self.model = Hometask.objects.create(
            lesson=Lesson.objects.create(
                **attrs.lesson_attrs,
                subject=Subject.objects.create(**attrs.subject_attrs),
                teacher=Teacher.objects.create(
                    **attrs.teacher_attrs,
                    faculty=Faculty.objects.create(**attrs.faculty_attrs)
                )
            ),
            **attrs.hometask_attrs,
        )
        self.to_change = attrs.hometask_new_attrs

    def test_create_model(self):
        """POST."""
        response = self.client.post(
            '/rest/hometask/',
            data=json.dumps(self.request_data),
            content_type='application/json'
        )
        serializer = HometaskSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_model(self):
        """GET."""
        url_to_get = f'/rest/hometask/{self.model.id}/'
        response = self.client.get(url_to_get)
        serializer = HometaskSerializer(data=self.request_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_model(self):
        """PUT."""
        url_to_update = f'/rest/hometask/{self.model.id}/'
        response = self.client.patch(
            url_to_update,
            data=json.dumps(
                self.to_change,
            ),
            content_type='application/json'
        )
        serializer = HometaskSerializer(data=self.to_change, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_model(self):
        """DELETE."""
        url_to_delete = f'/rest/hometask/{self.model.id}/'
        response = self.client.delete(url_to_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Hometask.objects.filter(id=self.model.id).exists()
        )
