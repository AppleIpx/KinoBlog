# Generated by Django 4.2.10 on 2024-04-25 14:17

from django.db import migrations
import some_proj.blog.snippets.film_snippet
import some_proj.blog.snippets.serial_snippet
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blogpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.fields.StreamField([('text', wagtail.blocks.RichTextBlock(features=['h1', 'h2', 'h3', 'bold', 'italic', 'hr', 'blockquote'], help_text='Введите описание', label='Текст')), ('images', wagtail.blocks.StructBlock([('image', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(help_text='Загрузите изображение', icon='image', label='Изображение'))), ('title', wagtail.blocks.CharBlock(blank=True, label='Заголовок', required=False)), ('description', wagtail.blocks.CharBlock(blank=True, label='Описание', required=False))])), ('content', wagtail.embeds.blocks.EmbedBlock(help_text='Пример ссылки: https://www.youtube.com/watch?v=5mM0fX_kKCU', label='Ссылка на видео контент')), ('film', wagtail.blocks.StructBlock([('film', wagtail.snippets.blocks.SnippetChooserBlock(some_proj.blog.snippets.film_snippet.FilmBlogModel, label='Выберите фильм')), ('film_fields', wagtail.blocks.MultipleChoiceBlock(choices=[('Название', 'Название'), ('Постер', 'Постер'), ('Страны', 'Страны'), ('Жанры', 'Жанры'), ('Описание', 'Описание'), ('Трейлер', 'Трейлер'), ('Кадры', 'Кадры'), ('Актёры', 'Актёры'), ('Длительность', 'Длительность'), ('Режиссёр', 'Режиссёр')], label='Выберите поле для отображения'))])), ('serial', wagtail.blocks.StructBlock([('serial', wagtail.snippets.blocks.SnippetChooserBlock(some_proj.blog.snippets.serial_snippet.SerialBlogModel, label='Выберите сериал')), ('serial_fields', wagtail.blocks.MultipleChoiceBlock(choices=[('Название', 'Название'), ('Постер', 'Постер'), ('Страны', 'Страны'), ('Жанры', 'Жанры'), ('Описание', 'Описание'), ('Трейлер', 'Трейлер'), ('Кадры', 'Кадры'), ('Актёры', 'Актёры'), ('Длительность', 'Длительность'), ('Режиссёр', 'Режиссёр'), ('Сезон', 'Сезон'), ('Количество серий', 'Количество серий')], label='Выберите поле для отображения'))]))], blank=True, verbose_name='Место для творчества'),
        ),
    ]
