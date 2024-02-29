# получаем предыдущую версию медии
def get_previous_media(instance):
    return instance.history.first()
