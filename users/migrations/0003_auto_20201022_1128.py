# Generated by Django 3.0.6 on 2020-10-22 05:58

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='resume',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]