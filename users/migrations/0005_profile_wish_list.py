# Generated by Django 3.0.6 on 2020-10-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_jobs', '0010_auto_20201022_1128'),
        ('users', '0004_invite'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='wish_list',
            field=models.ManyToManyField(blank=True, default=None, related_name='wish_list', to='my_jobs.Job'),
        ),
    ]
