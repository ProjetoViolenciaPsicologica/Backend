# Generated by Django 4.0.6 on 2024-03-19 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psicoapp', '0009_remove_formulario_grau_de_instrucao'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulario',
            name='grauInstrucao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='psicoapp.grauinstrucao'),
        ),
    ]