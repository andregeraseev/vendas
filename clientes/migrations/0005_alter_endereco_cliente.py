# Generated by Django 4.1.3 on 2022-11-02 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_endereco_apelido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente'),
            preserve_default=False,
        ),
    ]
