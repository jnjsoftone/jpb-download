# JnJ File Downloader API

Chrome 확장 프로그램용 로컬 파일 다운로드 서버. FastAPI + yt-dlp 기반.

---

## 사전 준비

### 1. uv 설치 (Python 패키지 매니저)

**Windows (PowerShell)**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. ffmpeg 설치 (영상+오디오 병합에 필요)

**Windows**
```powershell
winget install --id Gyan.FFmpeg --source winget
```
설치 후 `downloader.py`의 `FFMPEG_PATH`를 실제 경로로 수정합니다.
```python
# downloader.py
FFMPEG_PATH = r"C:\Users\<사용자명>\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_...\bin"
```
> 정확한 경로 확인: `where ffmpeg` (설치 후 새 터미널에서 실행)

**macOS (Homebrew)**
```bash
brew install ffmpeg
```
macOS/Linux는 ffmpeg이 PATH에 자동 등록되므로 `FFMPEG_PATH` 설정이 필요 없습니다.
`downloader.py`에서 해당 줄을 아래와 같이 변경합니다.
```python
FFMPEG_PATH = ""   # 빈 문자열 → yt-dlp가 PATH에서 자동 탐색
```

**Linux (Ubuntu/Debian)**
```bash
sudo apt install ffmpeg
```

**Linux (Fedora)**
```bash
sudo dnf install ffmpeg
```

**Linux (Arch)**
```bash
sudo pacman -S ffmpeg
```

### 3. 프로젝트 의존성 설치

```bash
cd jnj-file-downloader
uv sync
```

### 4. 인증 토큰 설정

`main.py`의 `SECRET_TOKEN`을 원하는 값으로 변경합니다.

```python
# main.py
SECRET_TOKEN = "my-secret"   # 변경 권장
```

---

## 실행

```bash
uv run python -m uvicorn main:app --reload
```

API 문서: http://127.0.0.1:8000/api/docs

---

## 인증

모든 요청에 `x-token` 헤더 필요. `main.py`의 `SECRET_TOKEN` 값과 일치해야 합니다.

```
x-token: my-secret
```

---

## 엔드포인트

### `POST /download` — 자동 감지 다운로드

URL을 분석해 YouTube/video면 yt-dlp, 그 외는 직접 다운로드.

```json
{
  "url": "https://www.youtube.com/watch?v=xxxxx",
  "directory": "D:/Downloads",
  "type": "auto"
}
```

`type` 값: `auto` · `youtube` · `video` · `image` · `file`

---

### `POST /download/direct` — URL 직접 다운로드

이미지, 파일, 텍스트 등 일반 URL을 스트리밍으로 저장.

```json
{
  "url": "https://example.com/photo.jpg",
  "directory": "D:/Downloads",
  "filename": "photo.jpg",
  "headers": { "Referer": "https://example.com" }
}
```

---

### `POST /download/youtube` — YouTube / HLS / m3u8 다운로드

yt-dlp 기반. 해상도·오디오 품질·자막·재생목록 옵션 지원.

```json
{
  "url": "https://www.youtube.com/watch?v=xxxxx",
  "directory": "D:/Downloads",
  "quality": "1080p",
  "audio_quality": "high",
  "subtitles": "ko",
  "playlist_items": "1-5",
  "cookies_from_browser": "chrome"
}
```

| 파라미터 | 값 |
|---|---|
| `quality` | `best` · `1080p` · `720p` · `480p` · `360p` · `audio` |
| `audio_quality` | `best` · `high` (192k+) · `medium` (128k+) · `low` (64k+) |
| `subtitles` | `ko` · `en` · `ko,en` · `all` · `null` (기본, 자막 없음) |
| `playlist_items` | `1-3` · `1,3,5` 등 |
| `cookies_from_browser` | `chrome` · `firefox` · `edge` |

---

### `POST /save/text` — 텍스트 직접 저장

URL 없이 문자열을 파일로 저장.

```json
{
  "content": "hello world",
  "directory": "D:/Downloads",
  "filename": "hello.txt",
  "encoding": "utf-8"
}
```

---

### `POST /save/binary` — 바이너리 직접 저장

Base64 인코딩 데이터를 파일로 저장. Chrome 확장의 Data URI(`data:image/png;base64,...`) 그대로 전달 가능.

```json
{
  "content": "data:image/png;base64,iVBORw0KGgo...",
  "directory": "D:/Downloads",
  "filename": "screenshot.png"
}
```

---

## 공통 파라미터

모든 엔드포인트에서 사용 가능한 선택 필드:

| 파라미터 | 기본값 | 설명 |
|---|---|---|
| `filename` | 자동 추출 | 저장 파일명 |
| `overwrite` | `false` | 파일 덮어쓰기 여부. `false`이면 409 반환 |
| `requester` | `null` | 요청자 식별자 (로깅용) |
| `source_page` | `null` | 트리거 페이지 URL (Referer 헤더로 활용) |

---

## 의존성

| 패키지 | 설치 방식 | 용도 |
|---|---|---|
| fastapi · uvicorn | `uv sync` | HTTP 서버 |
| yt-dlp | `uv sync` | YouTube / HLS / m3u8 다운로드 |
| requests | `uv sync` | 직접 URL 다운로드 |
| ffmpeg | 별도 설치 (OS별 상이) | 영상+오디오 병합 |
