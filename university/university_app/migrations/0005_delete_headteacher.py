# Generated by Django 4.1.7 on 2023-05-16 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('university_app', '0004_remove_headteacher_modified'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HeadTeacher',
        ),
    ]
