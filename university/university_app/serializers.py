from .models import Faculty, Group, Teacher, Lesson, Mark, Hometask, Subject, Student
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from django.contrib.auth.models import User


class FacultySerializer(ModelSerializer):

    class Meta:
        model = Faculty
        fields = ('id', 'title', 'description')


class GroupSerializer(ModelSerializer):
    faculty = FacultySerializer()

    def create(self, validated_data: dict):
        faculty = Faculty.objects.create(
            title=validated_data['faculty']['title']
        )
        return Group.objects.create(
            faculty=faculty,
            title=validated_data['title']
        )

    class Meta:
        model = Group
        fields = ('id', 'title', 'faculty', 'lessons', 'subjects')


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'password', 'is_superuser']


class TeacherSerializer(ModelSerializer):
    faculty = FacultySerializer()

    def create(self, validated_data: dict):
        faculty = Faculty.objects.create(
            title=validated_data['faculty']['title']
        )
        return Teacher.objects.create(
            faculty=faculty,
            full_name=validated_data['full_name']
        )

    class Meta:
        model = Teacher
        fields = ('id', 'full_name', 'subjects', 'faculty', 'user')


class StudentSerializer(ModelSerializer):
    group = GroupSerializer()

    def create(self, validated_data: dict):
        group = Group.objects.create(
            title=validated_data['group']['title'],
            faculty=Faculty.objects.create(
                **validated_data['group']['faculty'])
        )
        return Student.objects.create(
            group=group,
            full_name=validated_data['full_name'],
        )

    class Meta:
        model = Student
        fields = ('id', 'full_name', 'group', 'user')


class SubjectSerializer(ModelSerializer):

    class Meta:
        model = Subject
        fields = ('id', 'title', 'groups', 'teachers')


class LessonSerializer(ModelSerializer):
    subject = SubjectSerializer()
    teacher = TeacherSerializer()

    def create(self, validated_data: dict):
        subject = Subject.objects.create(
            title=validated_data['subject']['title']
        )
        teacher = Teacher.objects.create(
            faculty=Faculty.objects.create(
                **validated_data['teacher']['faculty']),
            full_name=validated_data['teacher']['full_name'])
        return Lesson.objects.create(
            day=validated_data['day'],
            precise_time=validated_data['precise_time'],
            subject=subject,
            teacher=teacher
        )

    class Meta:
        model = Lesson
        fields = ('id', 'day', 'precise_time', 'subject', 'teacher', 'groups')


class MarkSerializer(ModelSerializer):
    student = StudentSerializer()
    lesson = LessonSerializer()

    def create(self, validated_data: dict):
        teacher = Teacher.objects.create(
            full_name=validated_data['lesson']['teacher']['full_name'],
            faculty=Faculty.objects.create(
                **validated_data['lesson']['teacher']['faculty'])
        )
        student = Student.objects.create(
            full_name=validated_data['student']['full_name'],
            group=Group.objects.create(
                title=validated_data['student']['group']['title'],
                faculty=Faculty.objects.create(**validated_data['student']['group']['faculty']))
        )
        lesson = Lesson.objects.create(
            day=validated_data['lesson']['day'],
            precise_time=validated_data['lesson']['precise_time'],
            subject=Subject.objects.create(
                **validated_data['lesson']['subject']),
            teacher=teacher)

        return Mark.objects.create(
            mark=validated_data['mark'],
            presence=validated_data['presence'],
            student=student,
            lesson=lesson
        )

    class Meta:
        model = Mark
        fields = ('id', 'mark', 'presence', 'created',
                  'modified', 'student', 'lesson')


class HometaskSerializer(ModelSerializer):
    lesson = LessonSerializer()

    def create(self, validated_data: dict):
        teacher = Teacher.objects.create(
            full_name=validated_data['lesson']['teacher']['full_name'],
            faculty=Faculty.objects.create(
                **validated_data['lesson']['teacher']['faculty'])
        )
        lesson = Lesson.objects.create(
            day=validated_data['lesson']['day'],
            precise_time=validated_data['lesson']['precise_time'],
            subject=Subject.objects.create(
                **validated_data['lesson']['subject']),
            teacher=teacher)
        return Hometask.objects.create(
            task=validated_data['task'],
            lesson=lesson
        )

    class Meta:
        model = Hometask
        fields = ('id', 'task', 'created', 'lesson')
