# Generated by Django 3.0.6 on 2020-09-14 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_jobs', '0005_auto_20200914_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='my_jobs.Category'),
        ),
    ]
