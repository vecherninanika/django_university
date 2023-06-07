from django.test import TestCase
from university_app.models import Mark
from university_app.forms import AddMarkForm
from . import attrs


class MarkFormTests(TestCase):
    def setUp(self):
        new_fields = attrs.set_up(Mark)
        for field, value in new_fields.items():
            attrs.mark_attrs[field] = value

    def test_successful(self):
        form = AddMarkForm(attrs.mark_attrs['lesson'], data=attrs.mark_attrs)
        self.assertTrue(form.is_valid())

    def test_successful_without_mark(self):
        local_attrs = attrs.mark_attrs.copy()
        del local_attrs['mark']
        form = AddMarkForm(attrs.mark_attrs['lesson'], data=local_attrs)
        self.assertTrue(form.is_valid())

    def test_successful_without_presence(self):
        local_attrs = attrs.mark_attrs.copy()
        del local_attrs['presence']
        form = AddMarkForm(attrs.mark_attrs['lesson'], data=local_attrs)
        self.assertTrue(form.is_valid())

    def test_failing_no_student(self):
        local_attrs = attrs.mark_attrs.copy()
        del local_attrs['student']
        AddMarkForm(attrs.mark_attrs['lesson'], data=local_attrs)
        self.assertRaises(Mark.student.RelatedObjectDoesNotExist)

    def test_failing_no_lesson(self):
        local_attrs = attrs.mark_attrs.copy()
        del local_attrs['lesson']
        AddMarkForm(attrs.mark_attrs['lesson'], data=local_attrs)
        self.assertRaises(Mark.lesson.RelatedObjectDoesNotExist)

    def test_failing_no_mark_and_presence(self):
        local_attrs = attrs.mark_attrs.copy()
        del local_attrs['mark']
        del local_attrs['presence']
        form = AddMarkForm(attrs.mark_attrs['lesson'], data=local_attrs)
        errors = ['Mark and presence cannot be both empty']
        self.assertEqual(errors, form.errors['__all__'])
