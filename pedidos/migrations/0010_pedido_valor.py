# Generated by Django 4.1.3 on 2022-11-15 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0009_pedido_endereco'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='valor',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]