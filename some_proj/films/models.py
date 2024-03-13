from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from some_proj.media_for_kino_card.models import MediaFile

User = get_user_model()


class BaseUserRelation(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True


class BasePersonModel(models.Model):
    name = models.CharField(
        verbose_name="Имя",
        max_length=200,
    )
    surname = models.CharField(
        verbose_name="Фамилия",
        max_length=200,
    )
    patronymic = models.CharField(
        verbose_name="Отчество",
        max_length=200,
    )
    birthday = models.DateField(
        verbose_name="Дата рождения",
    )
    photo = models.FileField(
        verbose_name="Фото",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class ProducerModel(BasePersonModel):
    films_made = models.ManyToManyField(
        "FilmModel",
        verbose_name="Фильмы/сериалы",
        blank=True,
    )

    class Meta:
        verbose_name = "Продюсер"
        verbose_name_plural = "Продюсеры"

    def __str__(self):
        return self.name


class ActorModel(BasePersonModel):
    films_participated = models.ManyToManyField(
        "FilmModel",
        verbose_name="Участие актера в следующих фильмах",
        blank=True,
    )

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"

    def __str__(self):
        return self.name


class GenreModel(models.Model):
    name = models.CharField(
        verbose_name="Название жанра",
        max_length=256,
    )

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"

    def __str__(self):
        return self.name


class ReactionModel(models.Model):
    reaction = models.BooleanField(
        verbose_name="Лайк/Дизлайк",
    )

    class Meta:
        verbose_name = "реакцию"
        verbose_name_plural = "реакции"

    def __str__(self):
        return "Лайк" if self.reaction else "Дизлайк"


class CountryModel(models.Model):
    name = models.CharField(
        verbose_name="Название страны",
        max_length=256,
    )

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class BaseContentModel(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=226,
    )
    poster = models.ImageField(
        verbose_name="Постер",
        upload_to="posters/",
        blank=True,
    )
    trailer = models.CharField(
        verbose_name="Ссылка на трейлер из youtube",
        max_length=500,
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    age_limit = models.IntegerField(
        verbose_name="Возрастное ограничение",
    )
    country = models.ManyToManyField(
        CountryModel,
        verbose_name="Страны",
    )
    producers = models.ManyToManyField(
        ProducerModel,
        verbose_name="Режиссер",
    )
    genre = models.ManyToManyField(
        GenreModel,
        verbose_name="Жанры",
    )
    actors = models.ManyToManyField(
        ActorModel,
        verbose_name="Актеры",
    )
    reaction = models.ManyToManyField(
        ReactionModel,
        verbose_name="Лайк/Дизлайк",
        blank=True,
    )

    class Meta:
        abstract = True

    @property
    def like_count(self):
        return self.reaction.filter(reaction=True).count()

    @property
    def dislike_count(self):
        return self.reaction.filter(reaction=False).count()


class FilmModel(BaseContentModel):
    release_date = models.DateField(
        verbose_name="Дата выхода фильма",
    )
    duration = models.IntegerField(
        verbose_name="Длительность фильма",
    )

    class Meta:
        verbose_name = "фильм"
        verbose_name_plural = "фильмы"

    def __str__(self):
        return self.name


class PhotoFilm(models.Model):
    film = models.ForeignKey(
        FilmModel,
        verbose_name="Фильм",
        on_delete=models.CASCADE,
        related_name="cadrs",
    )
    photo_film = models.ImageField(
        upload_to="photos_films/",
        verbose_name="Кадр из фильма",
    )

    class Meta:
        verbose_name = "кадр в фильме"
        verbose_name_plural = "кадры из фильмов"

    def __str__(self):
        return f"кадр из {self.film.name}"


class FavoriteContent(BaseUserRelation):
    class Meta:
        verbose_name = "избранный контент"
        verbose_name_plural = "избранные контенты"

    def __str__(self):
        return f"{self.user} добавил {self.content_object.name}"


class IsContentWatch(BaseUserRelation):
    minutes = models.IntegerField(
        verbose_name="Минуты просмотра",
    )
    media = models.ForeignKey(
        MediaFile,
        verbose_name="Медиа",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "просмотренный контент"
        verbose_name_plural = "просмотренные контенты"

    def __str__(self):
        message_for_film = f"{self.user} смотрел {self.content_object.name} и остановился на {self.minutes}"
        message_for_serial = (
            f"{self.user} смотрел {self.content_object.name} и"
            f" остановился на {self.media.content_object.episode} серии на {self.minutes} минуте"
        )
        return message_for_serial if hasattr(self.content_object, "season") else message_for_film


class SeeLateContent(BaseUserRelation):
    class Meta:
        verbose_name = "добавленный фильм в посмотреть позже"
        verbose_name_plural = "добавленные фильмы в посмотеть позже"

    def __str__(self):
        return f"{self.user} добавил {self.content_object.name} в посмотреть позже"
