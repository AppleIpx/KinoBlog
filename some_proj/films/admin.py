from django.contrib import admin

from some_proj.films.models import ActorModel
from some_proj.films.models import CountryModel
from some_proj.films.models import FilmContentModel
from some_proj.films.models import GenreModel
from some_proj.films.models import ProducerModelBase
from some_proj.films.models import ReactionModel

admin.site.register(FilmContentModel)
admin.site.register(CountryModel)
admin.site.register(ActorModel)
admin.site.register(GenreModel)
admin.site.register(ReactionModel)
admin.site.register(ProducerModelBase)
