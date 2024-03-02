def check_instace_for_film_serial(instance):
    if hasattr(instance.content_object, "season"):
        content_name = (
            f"{instance.content_object.name}/{instance.content_object.season} сезон /{instance.episode} серия"
        )
    else:
        content_name = instance.content_object.name
    return content_name
