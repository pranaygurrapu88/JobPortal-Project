# Generated by Django 3.0.6 on 2020-10-22 05:58

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_jobs', '0009_auto_20201015_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='employee',
            field=models.ManyToManyField(blank=True, default=None, related_name='job_employee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=ckeditor.fields.RichTextField(default=None),
        ),
    ]