from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.db.models import Exists
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from rest_framework import mixins
from rest_framework import viewsets

from some_proj.films.models import FavoriteContent
from some_proj.films.models import IsContentWatch
from some_proj.films.models import SeeLateContent
from some_proj.media_for_kino_card.models import MediaFile


class BaseContentView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_mapping: dict[str, Any] = {
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
        model.content_type = content_type
        content_filters = {
            "content_type": content_type,
            "object_id": OuterRef("pk"),
            "user": user,
        }
        queryset = model.objects.annotate(
            like_count=Count("reaction", filter=Q(reaction__reaction=True)),
            dislike_count=Count("reaction", filter=Q(reaction__reaction=False)),
            is_favorite=Exists(FavoriteContent.objects.filter(**content_filters)),
            is_watched=Exists(IsContentWatch.objects.filter(**content_filters)),
            is_see_late=Exists(SeeLateContent.objects.filter(**content_filters)),
        )
        if role == "staff":
            queryset = queryset.annotate(
                data_added=Subquery(media_files_qs.values("data_added")[:1]),
            )
        return queryset
