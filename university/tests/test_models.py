from django.test import TestCase
from university_app.models import Faculty, Group, Subject, Teacher, Lesson, Student, Mark, Hometask
from .attrs import *
from django.db.utils import DataError
from django.core.exceptions import ValidationError
from django.db.models import Model


def create_model_tests(cls_model: Model, attrs: dict, failing_attrs: dict, error=DataError):
    class ModelTests(TestCase):
        def setUp(self):
            new_fields = set_up(cls_model)
            for field, value in new_fields.items():
                attrs[field] = value
                failing_attrs[field] = value

        def test_successful_creation(self):
            cls_model.objects.create(**attrs)

        def test_failing_creation(self):
            if cls_model in (Mark, Hometask):
                obj = cls_model.objects.create(**failing_attrs)
                self.assertRaises(error, obj.full_clean)
            else:
                with self.assertRaises(error):
                    cls_model.objects.create(**failing_attrs)

    return ModelTests


# tests creation (all attrs are located in attrs.py)
FacultyTests = create_model_tests(
    Faculty, faculty_attrs, faculty_failing_attrs)
GroupTests = create_model_tests(
    Group, group_attrs, group_failing_attrs)
SubjectTests = create_model_tests(
    Subject, subject_attrs, subject_failing_attrs)
TeacherTests = create_model_tests(
    Teacher, teacher_attrs, teacher_failing_attrs)
LessonTests = create_model_tests(
    Lesson, lesson_attrs, lesson_failing_attrs, ValidationError)
StudentTests = create_model_tests(
    Student, student_attrs, student_failing_attrs)
MarkTests = create_model_tests(
    Mark, mark_attrs, mark_failing_attrs, ValidationError)
HometaskTests = create_model_tests(
    Hometask, hometask_attrs, hometask_failing_attrs, ValidationError)
