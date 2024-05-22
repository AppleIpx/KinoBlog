import ffmpeg


def get_quality(filepath: str) -> int | None:
    probe = ffmpeg.probe(filepath)
    video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
    if video_stream is not None:
        return int(video_stream["height"])
    return None
