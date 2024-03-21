from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from some_proj.films.views import FilmsView
from some_proj.serials.views import SerialsView
from some_proj.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("films", FilmsView, basename="films")
router.register("serials", SerialsView, basename="serials")


app_name = "api"
urlpatterns = router.urls
