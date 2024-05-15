from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet

from some_proj.blog.views import BlockPageView
from some_proj.films.views import FilmsView
from some_proj.serials.views import SerialsView
from some_proj.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
api_router = WagtailAPIRouter("wagtailapi")

router.register("users", UserViewSet)
router.register("films", FilmsView, basename="films")
router.register("serials", SerialsView, basename="serials")
router.register("pages", BlockPageView, basename="pages")
api_router.register_endpoint("images", ImagesAPIViewSet)
api_router.register_endpoint("documents", DocumentsAPIViewSet)


app_name = "api"
urlpatterns = router.urls
