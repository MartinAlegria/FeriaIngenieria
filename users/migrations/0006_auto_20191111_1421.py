# Generated by Django 2.2.7 on 2019-11-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20191111_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacion',
            name='profesor',
            field=models.ManyToManyField(to='users.Profesor'),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='proyecto',
            field=models.ManyToManyField(to='feria_ing.Project'),
        ),
    ]
