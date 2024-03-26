import logging


def check_instace_for_film_serial(instance):
    if hasattr(instance.content_object, "season"):
        content_name = f"{instance.content_object.name}/{instance.content_object.season} сезон/{instance.episode} серия"
    else:
        content_name = instance.content_object.name
    content_name = content_name.replace(" ", "_")
    file_name = instance.content_object.name.replace(" ", "_")

    object_message = "Объект определен"
    logging.info(object_message)
    return content_name, file_name
