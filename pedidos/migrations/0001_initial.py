# Generated by Django 4.1.3 on 2022-11-03 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendedores', '0002_vendedor_created_at_vendedor_updated_at'),
        ('produtos', '0002_juice_created_at_juice_updated_at'),
        ('clientes', '0008_cliente_cpf'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
                ('produtos', models.ManyToManyField(to='produtos.juice')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendedores.vendedor')),
            ],
        ),
    ]
