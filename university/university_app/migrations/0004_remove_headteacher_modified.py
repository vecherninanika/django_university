# Generated by Django 4.1.7 on 2023-05-16 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('university_app', '0003_headteacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='headteacher',
            name='modified',
        ),
    ]