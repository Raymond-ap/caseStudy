# Generated by Django 4.0.3 on 2022-04-28 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcs', '0010_alter_projectassignment_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklog',
            name='bill_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
