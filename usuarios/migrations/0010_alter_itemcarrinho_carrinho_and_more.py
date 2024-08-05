# Generated by Django 5.0.4 on 2024-07-22 08:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_alter_carrinho_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcarrinho',
            name='carrinho',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='usuarios.carrinho'),
        ),
        migrations.AlterField(
            model_name='itemcarrinho',
            name='quantidade',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
