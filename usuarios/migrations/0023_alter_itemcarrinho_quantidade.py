# Generated by Django 5.0.4 on 2024-07-22 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0022_remove_carrinho_imagem_carrinho_produto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcarrinho',
            name='quantidade',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
