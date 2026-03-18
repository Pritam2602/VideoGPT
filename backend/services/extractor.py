import yt_dlp
import os


def download_audio(video_url: str, output_dir: str = "temp") -> str:
    """
    Download audio from any video URL using yt-dlp.
    Supports YouTube, Vimeo, and many other platforms.
    
    Returns the path to the downloaded audio file.
    """
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        video_id = info.get("id", "temp_audio")
        audio_path = os.path.join(output_dir, f"{video_id}.mp3")

    return audio_path
