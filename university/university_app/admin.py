from django.contrib import admin
from .models import Faculty, Group, Subject, Teacher, Lesson, Student, Mark, Hometask, LessonToGroup, SubjectToGroup, SubjectToTeacher


class LessonGroupInline(admin.TabularInline):
    model = LessonToGroup
    extra = 1


class SubjectGroupInline(admin.TabularInline):
    model = SubjectToGroup
    extra = 1


class SubjectTeacherInline(admin.TabularInline):
    model = SubjectToTeacher
    extra = 1


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    model = Faculty
    list_filter = (
        'title',
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    model = Group
    inlines = (SubjectGroupInline, LessonGroupInline)
    list_filter = (
        'faculty',
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    model = Subject
    inlines = (SubjectGroupInline, SubjectTeacherInline)
    list_filter = (
        'group',
        'teacher',
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    model = Teacher
    inlines = (SubjectTeacherInline,)
    list_filter = (
        'subject',
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    model = Lesson
    inlines = (LessonGroupInline,)
    list_filter = (
        'day',
        'subject',
        'teacher',
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_filter = (
        'group',
    )


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    model = Mark
    list_filter = (
        'mark',
        'presence',
        'student',
        'lesson',
    )


@admin.register(Hometask)
class HometaskAdmin(admin.ModelAdmin):
    model = Hometask
    list_filter = (
        'lesson',
    )
