# Generated by Django 4.1.1 on 2022-09-09 06:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviesapp', '0003_movie_is_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='is_public',
        ),
    ]
