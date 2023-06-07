from django.db import models
from uuid import uuid4
from datetime import datetime, timezone
from django.utils.translation import gettext_lazy as _
from . import config
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.conf.global_settings import AUTH_USER_MODEL


def get_datetime():
    return datetime.now(timezone.utc)


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


def validate_time(attr: datetime):
    if attr > now():
        raise ValidationError(
            'Created and modified cannot be dates in the future',
            params={'modified': attr}
        )


class CreatedMixin(models.Model):
    created = models.DateTimeField(_('created'), default=get_datetime, validators=[
                                   validate_time], blank=True, null=False)

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(_('modified'), default=get_datetime, validators=[
                                    validate_time], blank=True, null=False)

    class Meta:
        abstract = True


class Faculty(UUIDMixin):
    title = models.CharField(_('faculty'), max_length=config.CHARS_DEFAULT)
    description = models.TextField(_('description'), blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('faculty')
        verbose_name_plural = _('faculties')
        db_table = 'faculty'


class Group(UUIDMixin):
    title = models.CharField(_('group'), max_length=config.CHARS_DEFAULT)
    faculty = models.ForeignKey(Faculty, verbose_name=_(
        'faculty'), on_delete=models.CASCADE)
    lessons = models.ManyToManyField(
        'Lesson', verbose_name=_('lessons'), through='LessonToGroup')
    subjects = models.ManyToManyField(
        'Subject', verbose_name=_('subjects'), through='SubjectToGroup')

    def clean(self):
        # lesson-subject validation
        for lesson in self.lessons.all():
            if lesson.subject not in self.subjects.all():
                raise ValidationError(
                    f"The lesson {lesson} is not in the group's subjects"
                )

    def __str__(self):
        return f'{self.title} ({self.faculty})'

    class Meta:
        ordering = ['title']
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        db_table = 'class'


class Subject(UUIDMixin):
    title = models.CharField(_('title'), max_length=config.CHARS_DEFAULT)
    groups = models.ManyToManyField(
        Group, verbose_name=_('groups'), through='SubjectToGroup')
    teachers = models.ManyToManyField(
        'Teacher', verbose_name=_('teachers'), through='SubjectToTeacher')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')
        db_table = 'subject'


class Teacher(UUIDMixin):
    user = models.OneToOneField(
        AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(
        _('full name'), max_length=config.CHARS_DEFAULT)
    subjects = models.ManyToManyField(
        Subject, verbose_name=_('subjects'), through='SubjectToTeacher')
    faculty = models.ForeignKey(Faculty, verbose_name=_(
        'faculty'), on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['full_name']
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')
        db_table = 'teacher'


class Lesson(UUIDMixin):
    day = models.DateField(_('day'))
    precise_time = models.TimeField(_('precise time'))
    subject = models.ForeignKey(Subject, verbose_name=_(
        'subject'), on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, verbose_name=_(
        'teacher'), on_delete=models.CASCADE)
    groups = models.ManyToManyField(
        Group, verbose_name=_('groups'), through='LessonToGroup')

    def clean(self):
        # subject-teacher validation
        teachers = Teacher.objects.filter(subject__id=self.subject_id)
        if self.teacher not in teachers:
            raise ValidationError(
                f'The teacher {self.teacher} does not teach subject {self.subject}'
            )
        # subject-groups validation
        for group in self.groups.all():
            if self.subject not in group.subjects.all():
                raise ValidationError(
                    f"The group {group} does not have subject {self.subject}"
                )

    def __str__(self):
        return f'{self.day} {self.precise_time}, {self.subject}'

    class Meta:
        ordering = ['day']
        verbose_name = _('lesson')
        verbose_name_plural = _('lessons')
        db_table = 'lesson'


class Student(UUIDMixin, CreatedMixin):
    user = models.OneToOneField(
        AUTH_USER_MODEL,  null=True, on_delete=models.CASCADE)
    full_name = models.CharField(verbose_name=_(
        'full name'), max_length=config.CHARS_DEFAULT)
    group = models.ForeignKey(Group, verbose_name=_(
        'group'), on_delete=models.CASCADE, db_column='class_id', blank=True, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['full_name']
        verbose_name = _('student')
        verbose_name_plural = _('students')
        db_table = 'student'


def validate_mark(mark: int):
    if mark < 1 or mark > 5:
        raise ValidationError(
            f'Invalid format of mark: {mark}. Mark should be a number from 1 to 5.',
            params={'mark': mark}
        )


def validate_presence(presence: str):
    if presence:
        if presence != 'Н':
            raise ValidationError(
                f"Invalid format of presence: {presence}. Presence should be null or 'Н'.",
                params={'presence': presence}
            )


class Mark(UUIDMixin, CreatedMixin, ModifiedMixin):
    mark = models.IntegerField(_('mark'), choices=config.MARK_CHOICES,
                               blank=True, null=True, validators=[validate_mark])
    presence = models.CharField(_('presence'), max_length=config.CHARS_DEFAULT, blank=True,
                                null=True, choices=config.PRESENCE_CHOICES, validators=[validate_presence])
    student = models.ForeignKey(Student, verbose_name=_(
        'student'), on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, verbose_name=_(
        'lesson'), on_delete=models.CASCADE)

    def clean(self):
        # student-lesson validation
        groups = Group.objects.filter(lesson__id=self.lesson_id)
        if self.student.group not in groups:
            raise ValidationError(
                f'The student {self.student} is not in the group that had a lesson on {self.lesson}'
            )
        # mark-or-presence-added validation
        if not self.mark and not self.presence:
            raise ValidationError(
                'Mark and presence cannot be both empty'
            )

    def __str__(self):
        if self.mark:
            if self.presence:
                return f'{self.student}, {self.lesson}: {self.presence}, {self.mark}'
            return f'{self.student}, {self.lesson}: {self.mark}'
        return f'{self.student}, {self.lesson}: {self.presence}'

    class Meta:
        ordering = ['lesson']
        verbose_name = _('mark')
        verbose_name_plural = _('marks')
        db_table = 'mark'


class Hometask(UUIDMixin, CreatedMixin):
    task = models.TextField(_('task'))
    lesson = models.ForeignKey(Lesson, verbose_name=_(
        'lesson'), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.lesson}: {self.task}'

    class Meta:
        ordering = ['task']
        verbose_name = _('hometask')
        verbose_name_plural = _('hometasks')
        db_table = 'hometask'


class LessonToGroup(UUIDMixin):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, db_column='class_id')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        db_table = 'lesson_to_class'


class SubjectToGroup(UUIDMixin):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, db_column='class_id')

    class Meta:
        db_table = 'subject_to_class'
        unique_together = (('subject', 'group'),)


class SubjectToTeacher(UUIDMixin):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        db_table = 'subject_to_teacher'
        unique_together = (('subject', 'teacher'),)
