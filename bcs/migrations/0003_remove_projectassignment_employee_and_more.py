# Generated by Django 4.0.3 on 2022-04-06 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcs', '0002_remove_projectschedule_project_schedule_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectassignment',
            name='employee',
        ),
        migrations.AddField(
            model_name='projectassignment',
            name='employee',
            field=models.ManyToManyField(to='bcs.employee'),
        ),
    ]
