# Generated by Django 4.2.10 on 2024-04-23 14:41

from django.db import migrations, models
import django.db.models.deletion
import some_proj.media_for_kino_card.utils.shared_files.clean_poster
import some_proj.media_for_kino_card.utils.shared_files.generate_name_poster
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('surname', models.CharField(max_length=200, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=200, verbose_name='Отчество')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('photo', models.FileField(blank=True, null=True, upload_to=some_proj.media_for_kino_card.utils.shared_files.generate_name_poster.generate_filename_photos, verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'актер',
                'verbose_name_plural': 'актеры',
            },
        ),
        migrations.CreateModel(
            name='CountryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название страны')),
            ],
            options={
                'verbose_name': 'страна',
                'verbose_name_plural': 'страны',
            },
        ),
        migrations.CreateModel(
            name='FavoriteContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'избранный контент',
                'verbose_name_plural': 'избранные контенты',
            },
        ),
        migrations.CreateModel(
            name='FilmModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=226, verbose_name='Название')),
                ('poster', sorl.thumbnail.fields.ImageField(blank=True, upload_to=some_proj.media_for_kino_card.utils.shared_files.generate_name_poster.generate_filename_photos, validators=[some_proj.media_for_kino_card.utils.shared_files.clean_poster.poster_validator], verbose_name='Постер')),
                ('trailer', models.CharField(max_length=500, verbose_name='Ссылка на трейлер из youtube')),
                ('description', models.TextField(verbose_name='Описание')),
                ('age_limit', models.PositiveSmallIntegerField(verbose_name='Возрастное ограничение')),
                ('release_date', models.DateField(verbose_name='Дата выхода фильма')),
                ('duration', models.PositiveSmallIntegerField(verbose_name='Длительность фильма')),
            ],
            options={
                'verbose_name': 'фильм',
                'verbose_name_plural': 'фильмы',
            },
        ),
        migrations.CreateModel(
            name='GenreModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название жанра')),
            ],
            options={
                'verbose_name': 'жанр',
                'verbose_name_plural': 'жанры',
            },
        ),
        migrations.CreateModel(
            name='IsContentWatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('minutes', models.IntegerField(verbose_name='Минуты просмотра')),
            ],
            options={
                'verbose_name': 'просмотренный контент',
                'verbose_name_plural': 'просмотренные контенты',
            },
        ),
        migrations.CreateModel(
            name='PhotoFilm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_film', models.ImageField(upload_to=some_proj.media_for_kino_card.utils.shared_files.generate_name_poster.generate_filename_photos, verbose_name='Кадр из фильма')),
            ],
            options={
                'verbose_name': 'кадр в фильме',
                'verbose_name_plural': 'кадры из фильмов',
            },
        ),
        migrations.CreateModel(
            name='ProducerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('surname', models.CharField(max_length=200, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=200, verbose_name='Отчество')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('photo', models.FileField(blank=True, null=True, upload_to=some_proj.media_for_kino_card.utils.shared_files.generate_name_poster.generate_filename_photos, verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Продюсер',
                'verbose_name_plural': 'Продюсеры',
            },
        ),
        migrations.CreateModel(
            name='ReactionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('reaction', models.BooleanField(verbose_name='Лайк/Дизлайк')),
            ],
            options={
                'verbose_name': 'реакцию',
                'verbose_name_plural': 'реакции',
            },
        ),
        migrations.CreateModel(
            name='SeeLateContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'добавленный фильм в посмотреть позже',
                'verbose_name_plural': 'добавленные фильмы в посмотеть позже',
            },
        ),
    ]
