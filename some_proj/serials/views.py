from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from some_proj.serials.models import SerialModel
from some_proj.serials.serializers import AdminListAdminSerializer
from some_proj.serials.serializers import AdminSerialSerializer
from some_proj.serials.serializers import DetailedSerialGuestSerializer
from some_proj.serials.serializers import DetailedSerialSerializer
from some_proj.serials.serializers import ListSerialGuestSerializer
from some_proj.serials.serializers import ListSerialSerializer


class SerialsView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberPagination
    queryset = SerialModel.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        has_pk_param = bool(self.kwargs.get("pk"))
        if has_pk_param:
            self.action = "detailed"
        else:
            self.action = "list"
        role = "staff" if user.is_staff else "authenticated" if user.is_authenticated else "anonymous"

        serializer_mapping = {
            "staff": {
                "list": AdminListAdminSerializer,
                "detailed": AdminSerialSerializer,
            },
            "authenticated": {
                "list": ListSerialSerializer,
                "detailed": DetailedSerialSerializer,
            },
            "anonymous": {
                "list": ListSerialGuestSerializer,
                "detailed": DetailedSerialGuestSerializer,
            },
        }
        return serializer_mapping[role][self.action]
