# Generated by Django 3.0.6 on 2020-09-14 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_jobs', '0003_auto_20200914_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
