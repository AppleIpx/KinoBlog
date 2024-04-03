from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.db.models import Exists
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import viewsets

from some_proj.films.models import FavoriteContent
from some_proj.films.models import FilmModel
from some_proj.films.models import IsContentWatch
from some_proj.films.models import SeeLateContent
from some_proj.films.serializers.film_serializers import AdminFilmSerializer
from some_proj.films.serializers.film_serializers import AdminListFilmSerializer
from some_proj.films.serializers.film_serializers import DetailedFilmGuestSerializer
from some_proj.films.serializers.film_serializers import DetailedFilmSerializer
from some_proj.films.serializers.film_serializers import ListFilmGuestSerializer
from some_proj.films.serializers.film_serializers import ListFilmSerializer
from some_proj.media_for_kino_card.models import MediaFile


class BaseContentView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_mapping = {
        "list": None,
        "detailed": None,
    }

    def get_serializer_class(self):
        user = self.request.user
        has_pk_param = bool(self.kwargs.get("pk"))
        if has_pk_param:
            self.action = "detailed"
        else:
            self.action = "list"
        role = "staff" if user.is_staff else "authenticated" if user.is_authenticated else "anonymous"
        return self.serializer_mapping[role][self.action]

    def get_annotated_queryset(self, model, user, role):
        content_type = ContentType.objects.get_for_model(model)
        media_files_qs = MediaFile.objects.filter(
            content_type=content_type,
            object_id=OuterRef("pk"),
        ).order_by("id")
        queryset = model.objects.annotate(
            like_count=Count("reaction", filter=Q(reaction__reaction=True)),
            dislike_count=Count("reaction", filter=Q(reaction__reaction=False)),
            is_favorite=Exists(
                FavoriteContent.objects.filter(
                    content_type=content_type,
                    object_id=OuterRef("pk"),
                    user=user,
                ),
            ),
            is_watched=Exists(
                IsContentWatch.objects.filter(
                    content_type=content_type,
                    object_id=OuterRef("pk"),
                    user=user,
                ),
            ),
            is_see_late=Exists(
                SeeLateContent.objects.filter(
                    content_type=content_type,
                    object_id=OuterRef("pk"),
                    user=user,
                ),
            ),
        )
        if role == "staff":
            queryset = queryset.annotate(
                data_added=Subquery(media_files_qs.values("data_added")[:1]),
            )
        return queryset


@extend_schema(tags=["Films"])
class FilmsView(BaseContentView):
    serializer_mapping = {
        "staff": {
            "list": AdminListFilmSerializer,
            "detailed": AdminFilmSerializer,
        },
        "authenticated": {
            "list": ListFilmSerializer,
            "detailed": DetailedFilmSerializer,
        },
        "anonymous": {
            "list": ListFilmGuestSerializer,
            "detailed": DetailedFilmGuestSerializer,
        },
    }

    @extend_schema(
        description="Отображение списка фильмов",
        responses={
            200: AdminListFilmSerializer(),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Отображение конкретного фильма",
        responses={
            200: AdminFilmSerializer(),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.get_annotated_queryset(FilmModel, user, "staff")
        if user.is_authenticated:
            return self.get_annotated_queryset(FilmModel, user, "authenticated")
        return FilmModel.objects.all()
