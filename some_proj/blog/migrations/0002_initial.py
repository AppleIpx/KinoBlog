# Generated by Django 4.2.10 on 2024-04-23 14:41

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('films', '0001_initial'),
        ('blog', '0001_initial'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('serials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilmBlogModel',
            fields=[
            ],
            options={
                'verbose_name': 'фильм',
                'verbose_name_plural': 'фильмы',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('films.filmmodel',),
        ),
        migrations.CreateModel(
            name='FilmsCadrsModel',
            fields=[
            ],
            options={
                'verbose_name': 'кадр из фильма',
                'verbose_name_plural': 'кадры из фильмов',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('films.photofilm',),
        ),
        migrations.CreateModel(
            name='SerialBlogModel',
            fields=[
            ],
            options={
                'verbose_name': 'сериал',
                'verbose_name_plural': 'сериалы',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('serials.serialmodel',),
        ),
        migrations.AddField(
            model_name='slidesmodel',
            name='film_photos',
            field=models.ManyToManyField(blank=True, to='films.photofilm'),
        ),
        migrations.AddField(
            model_name='slidesmodel',
            name='serial_photos',
            field=models.ManyToManyField(blank=True, to='serials.photoserial'),
        ),
        migrations.AddField(
            model_name='blogtagpage',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='blog.blogpage'),
        ),
        migrations.AddField(
            model_name='blogtagpage',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='authors',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.authorblog'),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='tag',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blog.BlogTagPage', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='blockimages',
            name='blog',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='slides', to='blog.blogpage'),
        ),
        migrations.AddField(
            model_name='blockimages',
            name='figure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Картинка'),
        ),
        migrations.AddField(
            model_name='authorblog',
            name='author_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Изображение автора'),
        ),
        migrations.AddField(
            model_name='authorblog',
            name='profession',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, help_text='Выберите профессию', to='blog.profession', verbose_name='Профессию'),
        ),
    ]
