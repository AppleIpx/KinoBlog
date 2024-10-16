# Generated by Django 4.2.10 on 2024-05-19 10:01

from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('episode', models.CharField(max_length=255, verbose_name='Выбор эпизода фильма')),
                ('orig_path_file', models.CharField(max_length=300, verbose_name='Ссылка на исходный локальный файл / S3')),
                ('data_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'медия',
                'verbose_name_plural': 'медии',
            },
        ),
        migrations.CreateModel(
            name='Quality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Качество')),
            ],
            options={
                'verbose_name': 'качество',
                'verbose_name_plural': 'качества',
            },
        ),
        migrations.CreateModel(
            name='UrlsInMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default='', max_length=300, verbose_name='Ссылка')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_for_kino_card.mediafile', verbose_name='Медиа')),
                ('quality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_for_kino_card.quality', verbose_name='Качество')),
            ],
            options={
                'verbose_name': 'ссылка на локальный файл/амазон',
                'verbose_name_plural': 'ссылки на локальные файлы/амазон',
            },
        ),
        migrations.AddField(
            model_name='mediafile',
            name='urls',
            field=models.ManyToManyField(blank=True, related_name='media_urls', to='media_for_kino_card.urlsinmedia', verbose_name='Ссылки на видеофайлы'),
        ),
        migrations.CreateModel(
            name='HistoricalMediaFile',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('episode', models.CharField(max_length=255, verbose_name='Выбор эпизода фильма')),
                ('orig_path_file', models.CharField(max_length=300, verbose_name='Ссылка на исходный локальный файл / S3')),
                ('data_added', models.DateTimeField(blank=True, editable=False, verbose_name='Дата загрузки')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('content_type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'historical медия',
                'verbose_name_plural': 'historical медии',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
