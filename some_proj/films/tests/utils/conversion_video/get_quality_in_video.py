import ffmpeg


def get_quality(filepath):
    probe = ffmpeg.probe(filepath)
    video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
    return int(video_stream["height"])
