# Generated by Django 3.0.6 on 2020-11-11 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogging',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
