# Generated by Django 4.0.6 on 2024-02-26 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psicoapp', '0003_user_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalFormulario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('definicaoLocalForm', models.CharField(default='', max_length=255)),
            ],
            options={
                'verbose_name': 'Tipo de um usuário',
                'verbose_name_plural': 'Tipos de um usuário',
            },
        ),
    ]
