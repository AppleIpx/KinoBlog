from uuid import uuid4


def generate_filename_photos(instance, filename):
    ext = filename.split(".")[-1]
    new_filename = f"{uuid4().hex}.{ext}"
    return f"photos/{new_filename}"
