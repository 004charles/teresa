# Generated by Django 5.0.4 on 2024-07-25 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0033_marca_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.URLField()),
            ],
            options={
                'verbose_name_plural': 'Video Principal',
            },
        ),
    ]
