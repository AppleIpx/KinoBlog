from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PersonModel(models.Model):
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


class ProducerModel(PersonModel):
    class Meta:
        verbose_name = "Продюсер"
        verbose_name_plural = "Продюсеры"

    def __str__(self):
        return self.name


class ActorModel(PersonModel):
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
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class ReactionModel(models.Model):
    reaction = models.BooleanField(
        verbose_name="Лайк/Дизлайк",
    )

    class Meta:
        verbose_name = "Реакция"
        verbose_name_plural = "Реакции"

    def __str__(self):
        return self.reaction


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


class BaseModel(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=226,
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
    producer = models.ManyToManyField(
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


class FilmModel(BaseModel):
    release_date = models.DateField(
        verbose_name="Дата выхода фильма",
    )

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.name


class SerialModel(BaseModel):
    num_seasons = models.PositiveIntegerField(
        verbose_name="Кол-во сезонов",
    )
    num_serials = models.PositiveIntegerField(
        verbose_name="Кол-во серий",
    )

    class Meta:
        verbose_name = "Сериал"
        verbose_name_plural = "Сериалы"

    def __str__(self):
        return self.name
