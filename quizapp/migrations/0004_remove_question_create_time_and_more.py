# Generated by Django 4.1.4 on 2022-12-08 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('quizapp', '0003_questionset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='question',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='question',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='question',
            name='title',
        ),
        migrations.RemoveField(
            model_name='question',
            name='update_time',
        ),
        migrations.RemoveField(
            model_name='questionset',
            name='questions',
        ),
        migrations.AddField(
            model_name='question',
            name='content_type',
            field=models.ForeignKey(default=str, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='object_id',
            field=models.PositiveIntegerField(default=int),
            preserve_default=False,
        ),
    ]
