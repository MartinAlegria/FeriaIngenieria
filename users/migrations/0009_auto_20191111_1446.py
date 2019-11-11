# Generated by Django 2.2.7 on 2019-11-11 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feria_ing', '0001_initial'),
        ('users', '0008_auto_20191111_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluacion',
            name='profesor_id',
        ),
        migrations.RemoveField(
            model_name='evaluacion',
            name='proyecto_id',
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='profesor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='users.Profesor'),
        ),
        migrations.AddField(
            model_name='evaluacion',
            name='proyecto',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='feria_ing.Project'),
        ),
    ]