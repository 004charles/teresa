# Generated by Django 5.0.4 on 2024-07-29 20:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0035_alter_video_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='video',
            name='video',
            field=models.URLField(),
        ),
        migrations.CreateModel(
            name='Pedido_empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('endereco', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=50)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.empresas')),
            ],
        ),
    ]
