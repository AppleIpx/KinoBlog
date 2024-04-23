from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from some_proj.blog.snippets.film_snippet import DefaultPanels
from some_proj.serials.models import SerialModel


@register_snippet
class SerialBlogModel(SerialModel):
    panels = [
        *DefaultPanels,
        FieldPanel("season"),
        FieldPanel("num_serials"),
    ]

    class Meta:
        verbose_name = "сериал"
        verbose_name_plural = "сериалы"
        proxy = True

    def __str__(self):
        return f"{self.name} {self.season} сезон"
