# Generated by Django 4.0.6 on 2024-02-25 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psicoapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='psicoapp.areausuario'),
        ),
    ]
