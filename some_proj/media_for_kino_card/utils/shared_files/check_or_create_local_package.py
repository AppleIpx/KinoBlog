from pathlib import Path


def check_or_create_package(directory_path):
    path_obj = Path(directory_path)
    if not path_obj.exists():
        path_obj.mkdir(parents=True, exist_ok=True)
