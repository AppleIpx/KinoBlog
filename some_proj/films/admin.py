from django.contrib import admin

from some_proj.films.models import ActorModel
from some_proj.films.models import CountryModel
from some_proj.films.models import FavoriteContent
from some_proj.films.models import FilmModel
from some_proj.films.models import GenreModel
from some_proj.films.models import PhotoFilm
from some_proj.films.models import ProducerModel
from some_proj.films.models import ReactionModel

admin.site.register(FilmModel)
admin.site.register(CountryModel)
admin.site.register(ActorModel)
admin.site.register(GenreModel)
admin.site.register(ReactionModel)
admin.site.register(ProducerModel)
admin.site.register(PhotoFilm)
admin.site.register(FavoriteContent)
