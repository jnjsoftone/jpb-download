
"""
uv 로 python package를 관리하고, FastAPI, yt-dlp 등을 사용하여 file downloader를 구현하도록 해주세요. 필요시 file의 종류에 따라 별도의 로직을 구현하되, endpoint는 되도록이면 최소화해주세요.
"""


좋습니다 👍  
목표는:

> **uv 기반 Python 패키지 관리 + FastAPI + yt-dlp 기반 통합 File Downloader 서버**  
> ✔ endpoint 최소화  
> ✔ 파일 유형별 로직 분기  
> ✔ 이미지 / 일반 파일 / YouTube / m3u8 자동 처리

실전용 구조로 깔끔하게 설계해드리겠습니다.

---

# 1️⃣ 프로젝트 구조

file-downloader/  
 ├─ pyproject.toml  
 ├─ main.py  
 ├─ downloader.py  
 └─ utils.py

---

# 2️⃣ uv로 프로젝트 초기화

uv 사용

uv init file-downloader  
cd file-downloader  
  
uv add fastapi uvicorn yt-dlp requests python-multipart

실행:

uv run uvicorn main:app --reload

---

# 3️⃣ API 설계 (Endpoint 최소화)

## 단일 엔드포인트

POST /download

Body:

{  
  "url": "https://example.com/video",  
  "directory": "D:/Downloads",  
  "filename": "optional-name.mp4",  
  "type": "auto"   
}

`type` 옵션:

- `"auto"` (기본)
    
- `"image"`
    
- `"file"`
    
- `"video"`
    
- `"youtube"`
    

---

# 4️⃣ main.py

from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel  
from downloader import download_file  
  
app = FastAPI()  
  
class DownloadRequest(BaseModel):  
    url: str  
    directory: str  
    filename: str | None = None  
    type: str = "auto"  
  
@app.post("/download")  
async def download(req: DownloadRequest):  
    try:  
        result = download_file(  
            url=req.url,  
            directory=req.directory,  
            filename=req.filename,  
            file_type=req.type  
        )  
        return {"status": "success", "detail": result}  
    except Exception as e:  
        raise HTTPException(status_code=500, detail=str(e))

---

# 5️⃣ downloader.py

핵심 로직 분기

import os  
import requests  
import mimetypes  
import subprocess  
from urllib.parse import urlparse  
from utils import ensure_directory  
  
  
def download_file(url: str, directory: str, filename: str | None, file_type: str):  
  
    ensure_directory(directory)  
  
    if file_type == "auto":  
        file_type = detect_type(url)  
  
    if file_type in ["youtube", "video"]:  
        return download_video(url, directory)  
  
    if file_type == "image":  
        return download_binary(url, directory, filename)  
  
    if file_type == "file":  
        return download_binary(url, directory, filename)  
  
    raise ValueError("Unsupported file type")  
  
  
def detect_type(url: str):  
    if "youtube.com" in url or "youtu.be" in url:  
        return "youtube"  
  
    ext = os.path.splitext(urlparse(url).path)[1].lower()  
  
    if ext in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:  
        return "image"  
  
    if ext in [".mp4", ".mkv", ".webm"]:  
        return "video"  
  
    return "file"  
  
  
def download_binary(url, directory, filename):  
    response = requests.get(url, stream=True)  
    response.raise_for_status()  
  
    if not filename:  
        filename = os.path.basename(urlparse(url).path)  
  
    filepath = os.path.join(directory, filename)  
  
    with open(filepath, "wb") as f:  
        for chunk in response.iter_content(chunk_size=8192):  
            f.write(chunk)  
  
    return {"saved_to": filepath}  
  
  
def download_video(url, directory):  
    command = [  
        "yt-dlp",  
        "-P", directory,  
        url  
    ]  
  
    result = subprocess.run(command, capture_output=True, text=True)  
  
    if result.returncode != 0:  
        raise Exception(result.stderr)  
  
    return {"yt_dlp_output": result.stdout}

---

# 6️⃣ utils.py

import os  
  
def ensure_directory(path: str):  
    if not os.path.exists(path):  
        os.makedirs(path, exist_ok=True)

---

# 7️⃣ yt-dlp 설치 확인

yt-dlp 필요

uv로 설치했어도 CLI 필요:

uv run yt-dlp --version

또는 시스템 설치:

pip install -U yt-dlp

---

# 8️⃣ Extension에서 호출 예시

await fetch("http://127.0.0.1:8000/download", {  
  method: "POST",  
  headers: { "Content-Type": "application/json" },  
  body: JSON.stringify({  
    url: videoUrl,  
    directory: "D:/Media",  
    type: "auto"  
  })  
});

---

# 9️⃣ m3u8, HLS, DASH 지원

yt-dlp가 자동 처리합니다.

추가 옵션 넣고 싶으면:

command = [  
    "yt-dlp",  
    "-f", "bestvideo+bestaudio",  
    "--merge-output-format", "mp4",  
    "-P", directory,  
    url  
]

---

# 🔐 보안 강화 (권장)

내부 도구라도 토큰 추가하세요:

from fastapi import Header  
  
@app.post("/download")  
async def download(req: DownloadRequest, x_token: str = Header()):  
    if x_token != "my-secret":  
        raise HTTPException(status_code=401)

Extension에서:

headers: {  
  "Content-Type": "application/json",  
  "x-token": "my-secret"  
}

---

# 🚀 장점

- endpoint 1개
    
- 파일 유형 자동 감지
    
- 대용량 스트리밍 안전
    
- YouTube 완전 지원
    
- 확장 쉬움
    

---

# 🔥 확장 아이디어

- 다운로드 진행률 반환
    
- WebSocket 상태 스트리밍
    
- 파일명 자동 slug 변환
    
- Obsidian vault 자동 분류
    
- DB 로그 기록
    

---

# 🎯 최종 권장 구조

Chrome Extension  
   ↓  
FastAPI (uv 관리)  
   ↓  
yt-dlp / requests  
   ↓  
임의 디렉토리 저장

이 구조면 내부 자동화 플랫폼으로 충분히 확장 가능합니다 👍
