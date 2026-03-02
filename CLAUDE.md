# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Python backend server for a Chrome extension. Provides a local FastAPI server that the extension calls to download files (images, generic files, YouTube videos, HLS/m3u8 streams) to arbitrary local directories.

## Package Management

This project uses `uv` for all Python dependency management. Do not use `pip` directly.

```bash
# Initialize project (first time)
uv init file-downloader
cd file-downloader
uv add fastapi uvicorn yt-dlp requests python-multipart

# Run the server
uv run uvicorn main:app --reload

# Verify yt-dlp
uv run yt-dlp --version
```

## Intended File Structure

```
python/
├── pyproject.toml
├── main.py          # FastAPI app, single POST /download endpoint
├── downloader.py    # Type detection + dispatch logic
├── utils.py         # ensure_directory helper
└── docs/
    └── ai/chatgpt-web/chat01.md  # Original design conversation
```

## Architecture

**Single endpoint design:** `POST /download` handles all file types.

```json
{
  "url": "https://example.com/video",
  "directory": "D:/Downloads",
  "filename": "optional-name.mp4",
  "type": "auto"
}
```

**Type dispatch in `downloader.py`:**
- `"auto"` → `detect_type()` inspects URL for YouTube domains, then file extension
- `"youtube"` / `"video"` → `download_video()` via `yt-dlp` subprocess
- `"image"` / `"file"` → `download_binary()` via `requests` streaming

**yt-dlp** handles YouTube, m3u8/HLS, DASH automatically. For best quality use flags `-f bestvideo+bestaudio --merge-output-format mp4`.

## Chrome Extension Integration

The extension calls `http://127.0.0.1:8000/download` with a POST request. Security token via `x-token` header is recommended even for local use.

## Key Design Decisions

- Keep endpoints minimal — a single `/download` route handles all types via the `type` field
- yt-dlp is invoked as a subprocess (not as a Python library) to keep it isolated and easy to upgrade
- `requests` uses `stream=True` for safe large-file handling
- Directory creation is handled server-side via `ensure_directory()`
