from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

from schemas import AutoDownloadRequest, DirectDownloadRequest, YoutubeDownloadRequest, SaveTextRequest, SaveBinaryRequest
from downloader import download_auto, download_direct, download_youtube, save_text, save_binary

SECRET_TOKEN = "my-secret"

app = FastAPI(
    title="File Downloader API",
    description="""
Chrome 확장 프로그램용 로컬 파일 다운로드 서버.

## 엔드포인트

| 경로 | 용도 |
|---|---|
| `POST /download` | 타입 자동 감지 후 적절한 방식으로 다운로드 |
| `POST /download/direct` | URL 직접 다운로드 (이미지, 파일, 텍스트 등) |
| `POST /download/youtube` | YouTube / HLS / m3u8 다운로드 (yt-dlp) |
| `POST /save/text` | 텍스트 콘텐츠를 파일로 직접 저장 |
| `POST /save/binary` | Base64 바이너리 데이터를 파일로 직접 저장 |

## 인증

모든 요청에 `x-token` 헤더가 필요합니다.

```
x-token: my-secret
```

## quality 프리셋

`best` · `1080p` · `720p` · `480p` · `360p` · `audio`

## audio_quality 프리셋

`best` · `high` (192k+) · `medium` (128k+) · `low` (64k+)
""",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


def verify_token(x_token: str):
    if x_token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post(
    "/download",
    summary="자동 감지 다운로드",
    description="URL을 분석해 YouTube/video이면 yt-dlp로, 그 외에는 직접 다운로드합니다. `type` 필드로 강제 지정도 가능합니다.",
    tags=["Download"],
)
async def download(req: AutoDownloadRequest, x_token: str = Header(default="")):
    verify_token(x_token)
    try:
        result = download_auto(
            url=req.url,
            directory=req.directory,
            file_type=req.type,
            filename=req.filename,
            overwrite=req.overwrite,
            quality=req.quality,
            audio_quality=req.audio_quality,
            subtitles=req.subtitles,
            headers=req.headers,
            cookies_from_browser=req.cookies_from_browser,
            playlist_items=req.playlist_items,
            source_page=req.source_page,
        )
        return {"status": "success", "requester": req.requester, "detail": result}
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/download/direct",
    summary="직접 URL 다운로드",
    description="이미지, 파일, 텍스트 등 일반 URL을 스트리밍으로 다운로드합니다. `source_page`는 Referer 헤더로도 활용됩니다.",
    tags=["Download"],
)
async def download_direct_endpoint(req: DirectDownloadRequest, x_token: str = Header(default="")):
    verify_token(x_token)
    try:
        result = download_direct(
            url=req.url,
            directory=req.directory,
            filename=req.filename,
            overwrite=req.overwrite,
            headers=req.headers,
            source_page=req.source_page,
        )
        return {"status": "success", "requester": req.requester, "detail": result}
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/download/youtube",
    summary="YouTube / HLS / m3u8 다운로드",
    description="yt-dlp를 사용해 YouTube, HLS, DASH, m3u8 스트림을 다운로드합니다. 해상도·오디오 품질·자막·재생목록 옵션을 지원합니다.",
    tags=["Download"],
)
async def download_youtube_endpoint(req: YoutubeDownloadRequest, x_token: str = Header(default="")):
    verify_token(x_token)
    try:
        result = download_youtube(
            url=req.url,
            directory=req.directory,
            quality=req.quality,
            audio_quality=req.audio_quality,
            subtitles=req.subtitles,
            overwrite=req.overwrite,
            cookies_from_browser=req.cookies_from_browser,
            playlist_items=req.playlist_items,
            source_page=req.source_page,
        )
        return {"status": "success", "requester": req.requester, "detail": result}
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/save/text",
    summary="텍스트 콘텐츠 저장",
    description="문자열 콘텐츠를 지정한 경로에 텍스트 파일로 직접 저장합니다. URL 없이 사용 가능합니다.",
    tags=["Save"],
)
async def save_text_endpoint(req: SaveTextRequest, x_token: str = Header(default="")):
    verify_token(x_token)
    try:
        result = save_text(
            content=req.content,
            directory=req.directory,
            filename=req.filename,
            encoding=req.encoding,
            overwrite=req.overwrite,
        )
        return {"status": "success", "requester": req.requester, "detail": result}
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/save/binary",
    summary="바이너리 콘텐츠 저장",
    description="Base64로 인코딩된 바이너리 데이터를 파일로 저장합니다. `data:image/png;base64,...` 형식의 Data URI도 지원합니다.",
    tags=["Save"],
)
async def save_binary_endpoint(req: SaveBinaryRequest, x_token: str = Header(default="")):
    verify_token(x_token)
    try:
        result = save_binary(
            content=req.content,
            directory=req.directory,
            filename=req.filename,
            overwrite=req.overwrite,
        )
        return {"status": "success", "requester": req.requester, "detail": result}
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
