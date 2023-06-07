from university_app.models import Faculty, Group, Subject, Teacher, Lesson, Student, Mark, Hometask
from university_app.config import CHARS_DEFAULT
from random import sample, choice
from string import ascii_letters
from django.contrib.auth.models import User
from django.db.models import Model


def set_up(cls_model: Model):
    new_fields = {}
    faculty = {'title': 'Linguistics'}
    fc = Faculty.objects.create(**faculty)
    group = {'title': '7.1', 'faculty': fc}
    gr = Group.objects.create(**group)
    subject = {'title': 'English'}
    su = Subject.objects.create(**subject)
    teacher = {'full_name': 'Dennis Keller', 'faculty': fc}
    te = Teacher.objects.create(**teacher)
    us = User.objects.create(
        is_superuser=True,
        id=1000,
        username='test2',
        first_name='test2',
        last_name='test2',
        email='test2@mail.ru',
        password='test2'
    )
    if cls_model in (Group, Teacher):
        new_fields['faculty'] = fc
    if cls_model is Lesson:
        new_fields['subject'] = su
        new_fields['teacher'] = te
    if cls_model in (Mark, Hometask):
        lesson = {'day': '2023-04-07', 'precise_time': '14:45:00',
                  'subject': su, 'teacher': te}
        le = Lesson.objects.create(**lesson)
        le.groups.set((gr,))
        new_fields['lesson'] = le
    if cls_model is Mark:
        student = {'full_name': 'Steven Wright', 'group': gr}
        st = Student.objects.create(**student)
        new_fields['student'] = st
    if cls_model is Student:
        new_fields['group'] = gr
        new_fields['user'] = us
    return new_fields


# normal and failing values for attrs
normal_title = ''.join(sample(ascii_letters, CHARS_DEFAULT - 1))
failing_title = ''.join(sample(ascii_letters, CHARS_DEFAULT + 1))
new_title = ''.join(sample(ascii_letters, CHARS_DEFAULT - 1))
normal_mark = 5
new_mark = None
normal_presence = 'Н'
failing_mark = 6
failing_presence = choice(ascii_letters)


# dictionaries with attrs
subject_attrs = {'title': normal_title}
subject_failing_attrs = {'title': failing_title}
subject_new_attrs = {'title': new_title}

student_attrs = {'full_name': normal_title}
student_failing_attrs = {'full_name': failing_title}
student_new_attrs = {'full_name': new_title}

teacher_attrs = {'full_name': normal_title}
teacher_failing_attrs = {'full_name': failing_title}
teacher_new_attrs = {'full_name': new_title}

faculty_attrs = {'title': normal_title, 'description': normal_title}
faculty_failing_attrs = {'title': failing_title, 'description': normal_title}
faculty_new_attrs = {'title': normal_title, 'description': failing_title}

lesson_attrs = {'day': '2023-12-31', 'precise_time': '09:45:00'}
lesson_failing_attrs = {'day': '2023-13-40', 'precise_time': '24:70:61'}
lesson_new_attrs = {'day': '2023-11-30', 'precise_time': '09:00:00'}

mark_attrs = {'mark': normal_mark, 'presence': normal_presence}
mark_failing_attrs = {'mark': failing_mark, 'presence': failing_presence}
mark_new_attrs = {'mark': new_mark, 'presence': normal_presence}

group_attrs = {'title': normal_title}
group_failing_attrs = {'title': failing_title}
group_new_attrs = {'title': new_title}

hometask_attrs = {'task': normal_title}
hometask_failing_attrs = {}
hometask_new_attrs = {'task': new_title}
