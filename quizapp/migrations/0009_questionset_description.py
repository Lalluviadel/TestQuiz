# Generated by Django 4.1.4 on 2022-12-08 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0008_alter_question_answer_01_alter_question_answer_02_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionset',
            name='description',
            field=models.TextField(blank=True, verbose_name='описание'),
        ),
    ]