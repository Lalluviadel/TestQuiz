# Generated by Django 4.1.4 on 2022-12-08 14:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0004_remove_question_create_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='content',
            field=models.CharField(default='question', max_length=250),
        ),
        migrations.AddField(
            model_name='question',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='время создания'),
        ),
        migrations.AddField(
            model_name='question',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='активен'),
        ),
        migrations.AddField(
            model_name='question',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='время изменения'),
        ),
    ]