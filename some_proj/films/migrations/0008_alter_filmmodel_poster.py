# Generated by Django 4.2.10 on 2024-03-20 19:13

from django.db import migrations, models
import some_proj.films.models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0007_alter_filmmodel_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmmodel',
            name='poster',
            field=models.ImageField(blank=True, upload_to=some_proj.films.models.generate_filename_photos, verbose_name='Постер'),
        ),
    ]
