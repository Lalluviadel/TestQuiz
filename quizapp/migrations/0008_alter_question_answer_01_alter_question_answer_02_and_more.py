# Generated by Django 4.1.4 on 2022-12-08 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0007_rename_content_question_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer_01',
            field=models.CharField(blank=True, max_length=150, verbose_name='ответ №1'),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_02',
            field=models.CharField(blank=True, max_length=150, verbose_name='ответ №2'),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_03',
            field=models.CharField(blank=True, max_length=150, verbose_name='ответ №3'),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer_04',
            field=models.CharField(blank=True, max_length=150, verbose_name='ответ №4'),
        ),
    ]
