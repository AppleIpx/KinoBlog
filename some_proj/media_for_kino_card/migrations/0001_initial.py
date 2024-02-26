# Generated by Django 4.2.10 on 2024-02-22 14:48

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
                ('orig_file', models.URLField(verbose_name='Ссылка на S3')),
                ('data_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Медия',
                'verbose_name_plural': 'Медии',
            },
        ),
        migrations.CreateModel(
            name='Quality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Качество',
                'verbose_name_plural': 'Качества',
            },
        ),
        migrations.CreateModel(
            name='UrlsAmazonInMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_for_kino_card.mediafile', verbose_name='Медиа')),
                ('quality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_for_kino_card.quality', verbose_name='качество')),
            ],
            options={
                'verbose_name': 'Ссылка на амазон',
                'verbose_name_plural': 'Ссылки на амазон',
            },
        ),
        migrations.AddField(
            model_name='mediafile',
            name='urls',
            field=models.ManyToManyField(related_name='media_urls', to='media_for_kino_card.urlsamazoninmedia', verbose_name='Ссылки на файл в Amazon'),
        ),
        migrations.CreateModel(
            name='HistoricalMediaFile',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('episode', models.CharField(max_length=255, verbose_name='Выбор эпизода фильма')),
                ('orig_file', models.URLField(verbose_name='Ссылка на S3')),
                ('data_added', models.DateTimeField(blank=True, editable=False, verbose_name='Дата загрузки')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('content_type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'historical Медия',
                'verbose_name_plural': 'historical Медии',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
