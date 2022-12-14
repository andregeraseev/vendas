# Generated by Django 4.1.3 on 2022-11-01 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Juice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('mls', models.IntegerField()),
                ('mg', models.CharField(choices=[('0mg', '0'), ('3mg', '3'), ('6mg', '6'), ('9mg', '9'), ('12mg', '12')], default='0', max_length=4)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=8)),
                ('descricao', models.TextField(max_length=800)),
                ('criado', models.DateField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='static/juices')),
            ],
        ),
    ]
