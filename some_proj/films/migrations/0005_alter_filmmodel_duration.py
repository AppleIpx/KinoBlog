# Generated by Django 4.2.10 on 2024-03-20 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0004_alter_filmmodel_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmmodel',
            name='duration',
            field=models.PositiveIntegerField(verbose_name='Длительность фильма'),
        ),
    ]
