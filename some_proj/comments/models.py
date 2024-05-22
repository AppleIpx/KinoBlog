from django.contrib.auth import get_user_model
from django.db import models

from some_proj.films.models import BaseUserRelation

User = get_user_model()


class CommentModel(BaseUserRelation):
    user: User | None  # type: ignore[valid-type]
    text = models.TextField(
        verbose_name="Комментарий",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания комментария",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    def __str__(self):
        if self.user is not None and self.user.first_name is not None:
            return f"Комментарий от {self.user.first_name} в {self.content_object.name}"
        return "Пользователь не определен"
