import base64
import os
import subprocess
import requests
from urllib.parse import urlparse
from utils import ensure_directory


FFMPEG_PATH = r"C:\Users\Jungsam\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"

VIDEO_HEIGHT: dict[str, int | None] = {
    "best":  None,
    "1080p": 1080,
    "720p":  720,
    "480p":  480,
    "360p":  360,
    "audio": None,
}

AUDIO_BITRATE: dict[str, str] = {
    "best":   "",
    "high":   "[abr>=192]",
    "medium": "[abr>=128]",
    "low":    "[abr>=64]",
}


def build_format(quality: str, audio_quality: str) -> str:
    af = AUDIO_BITRATE.get(audio_quality, "")

    if quality == "audio":
        return f"bestaudio[ext=m4a]{af}/bestaudio{af}/best"

    height = VIDEO_HEIGHT.get(quality)
    vf = f"[height<={height}]" if height else ""

    return (
        f"bestvideo{vf}[ext=mp4]+bestaudio[ext=m4a]{af}"
        f"/bestvideo{vf}+bestaudio{af}"
        f"/best{vf}/best"
    )


def detect_type(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"

    ext = os.path.splitext(urlparse(url).path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        return "image"

    if ext in [".mp4", ".mkv", ".webm", ".m3u8", ".mpd"]:
        return "video"

    return "file"


def download_direct(
    url: str,
    directory: str,
    filename: str | None = None,
    overwrite: bool = False,
    headers: dict[str, str] | None = None,
    source_page: str | None = None,
) -> dict:
    ensure_directory(directory)

    if not filename:
        filename = os.path.basename(urlparse(url).path) or "download"

    filepath = os.path.join(directory, filename)

    if not overwrite and os.path.exists(filepath):
        raise FileExistsError(f"파일이 이미 존재합니다: {filepath}")

    req_headers: dict[str, str] = {}
    if source_page:
        req_headers["Referer"] = source_page
    if headers:
        req_headers.update(headers)

    response = requests.get(url, stream=True, headers=req_headers or None)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    return {"saved_to": filepath}


def download_youtube(
    url: str,
    directory: str,
    quality: str = "best",
    audio_quality: str = "best",
    subtitles: str | None = None,
    overwrite: bool = False,
    cookies_from_browser: str | None = None,
    playlist_items: str | None = None,
    source_page: str | None = None,
) -> dict:
    ensure_directory(directory)

    fmt = build_format(quality, audio_quality)
    output_ext = "m4a" if quality == "audio" else "mp4"

    command = [
        "yt-dlp",
        "-f", fmt,
        "--merge-output-format", output_ext,
        "--ffmpeg-location", FFMPEG_PATH,
        "-P", directory,
    ]

    command.append("--force-overwrites" if overwrite else "--no-overwrites")

    if subtitles:
        command += [
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs", subtitles,
            "--sub-format", "srt/vtt/best",
            "--embed-subs",
        ]

    if cookies_from_browser:
        command += ["--cookies-from-browser", cookies_from_browser]

    if playlist_items:
        command += ["--playlist-items", playlist_items]

    if source_page:
        command += ["--referer", source_page]

    command.append(url)

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(result.stderr)

    return {"yt_dlp_output": result.stdout}


def save_text(
    content: str,
    directory: str,
    filename: str,
    encoding: str = "utf-8",
    overwrite: bool = False,
) -> dict:
    ensure_directory(directory)

    filepath = os.path.join(directory, filename)

    if not overwrite and os.path.exists(filepath):
        raise FileExistsError(f"파일이 이미 존재합니다: {filepath}")

    with open(filepath, "w", encoding=encoding) as f:
        f.write(content)

    return {"saved_to": filepath, "size": len(content.encode(encoding))}


def save_binary(
    content: str,
    directory: str,
    filename: str,
    overwrite: bool = False,
) -> dict:
    ensure_directory(directory)

    filepath = os.path.join(directory, filename)

    if not overwrite and os.path.exists(filepath):
        raise FileExistsError(f"파일이 이미 존재합니다: {filepath}")

    # data URI (data:image/png;base64,...) 또는 순수 Base64 모두 처리
    if content.startswith("data:"):
        content = content.split(",", 1)[1]

    raw = base64.b64decode(content)

    with open(filepath, "wb") as f:
        f.write(raw)

    return {"saved_to": filepath, "size": len(raw)}


def download_auto(
    url: str,
    directory: str,
    file_type: str = "auto",
    filename: str | None = None,
    overwrite: bool = False,
    quality: str = "best",
    audio_quality: str = "best",
    subtitles: str | None = None,
    headers: dict[str, str] | None = None,
    cookies_from_browser: str | None = None,
    playlist_items: str | None = None,
    source_page: str | None = None,
) -> dict:
    if file_type == "auto":
        file_type = detect_type(url)

    if file_type in ["youtube", "video"]:
        return download_youtube(
            url=url,
            directory=directory,
            quality=quality,
            audio_quality=audio_quality,
            subtitles=subtitles,
            overwrite=overwrite,
            cookies_from_browser=cookies_from_browser,
            playlist_items=playlist_items,
            source_page=source_page,
        )

    return download_direct(
        url=url,
        directory=directory,
        filename=filename,
        overwrite=overwrite,
        headers=headers,
        source_page=source_page,
    )
