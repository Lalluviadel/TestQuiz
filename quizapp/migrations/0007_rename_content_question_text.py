# Generated by Django 4.1.4 on 2022-12-08 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0006_alter_category_description_alter_question_answer_01_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='content',
            new_name='text',
        ),
    ]
