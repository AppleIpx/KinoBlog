# Generated by Django 4.2.10 on 2024-03-13 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_for_kino_card', '0003_alter_historicalmediafile_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('films', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genremodel',
            options={'verbose_name': 'жанр', 'verbose_name_plural': 'жанры'},
        ),
        migrations.AlterModelOptions(
            name='producermodel',
            options={'verbose_name': 'Продюсер', 'verbose_name_plural': 'Продюсеры'},
        ),
        migrations.AlterField(
            model_name='actormodel',
            name='films_participated',
            field=models.ManyToManyField(blank=True, to='films.filmmodel', verbose_name='Участие актера в следующих фильмах'),
        ),
        migrations.AlterField(
            model_name='favoritecontent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='filmmodel',
            name='duration',
            field=models.IntegerField(verbose_name='Длительность фильма'),
        ),
        migrations.AlterField(
            model_name='iscontentwatch',
            name='media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_for_kino_card.mediafile', verbose_name='Медиа'),
        ),
        migrations.AlterField(
            model_name='iscontentwatch',
            name='minutes',
            field=models.IntegerField(verbose_name='Минуты просмотра'),
        ),
        migrations.AlterField(
            model_name='iscontentwatch',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='photofilm',
            name='film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cadrs', to='films.filmmodel', verbose_name='Фильм'),
        ),
        migrations.AlterField(
            model_name='photofilm',
            name='photo_film',
            field=models.ImageField(upload_to='media/photos_films/None', verbose_name='Кадр из фильма'),
        ),
        migrations.AlterField(
            model_name='producermodel',
            name='films_made',
            field=models.ManyToManyField(blank=True, to='films.filmmodel', verbose_name='Фильмы/сериалы'),
        ),
        migrations.AlterField(
            model_name='seelatecontent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
