# Generated by Django 4.2.10 on 2024-03-20 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0009_alter_filmmodel_age_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmmodel',
            name='age_limit',
            field=models.PositiveSmallIntegerField(verbose_name='Возрастное ограничение'),
        ),
    ]
