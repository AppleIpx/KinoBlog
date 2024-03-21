from urllib.parse import urlparse


def extract_name(output_folder, s3_path_to_file):
    parts = output_folder.split("/")
    output_folder = f"{output_folder}{parts[-2]}.mp4"
    parsed_url = urlparse(s3_path_to_file).path
    filename = parsed_url[parsed_url.index("orig_videos") :]
    return filename, output_folder
