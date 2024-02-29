from django.contrib import admin

from some_proj.media_for_kino_card.models import MediaFile
from some_proj.media_for_kino_card.models import Quality
from some_proj.media_for_kino_card.models import UrlsInMedia

admin.site.register(MediaFile)
admin.site.register(Quality)
admin.site.register(UrlsInMedia)
