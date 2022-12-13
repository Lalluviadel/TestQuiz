# Generated by Django 4.1.4 on 2022-12-13 12:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cards_app', '0004_alter_card_options_alter_card_expiration_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='время создания')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='время изменения')),
                ('use_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='время использования')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='активен')),
                ('order_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('card_used', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards_app.card', to_field='title')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
