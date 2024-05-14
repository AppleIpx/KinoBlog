from io import BytesIO

from django.core.exceptions import ValidationError
from PIL import Image


def poster_validator(poster):
    if poster:
        image = Image.open(BytesIO(poster.read()))
        width, height = image.size
        if width >= height:
            error_message = "Высота изображения должна быть больше его ширины. Повторите попытку"
            raise ValidationError(error_message)
        if width < 1920:  # noqa: PLR2004
            error_message = "Ширина изображения должна быть больше 1920. Повторите попытку"
            raise ValidationError(error_message)
        return poster
    return None
