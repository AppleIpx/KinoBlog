from django.contrib import admin

from some_proj.serials.models import PhotoSerial
from some_proj.serials.models import SerialModel

admin.site.register(SerialModel)
admin.site.register(PhotoSerial)
