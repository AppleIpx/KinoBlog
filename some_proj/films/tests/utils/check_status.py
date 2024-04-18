from rest_framework.status import HTTP_200_OK


def check_status(response):
    assert response.status_code == HTTP_200_OK, f"Ошибка статуса, {response.status_code}, ожидалось {HTTP_200_OK}"
