from pydantic import BaseModel, Field


class BaseDownloadRequest(BaseModel):
    url: str = Field(..., description="다운로드할 URL")
    directory: str = Field(..., description="저장할 로컬 디렉터리 경로 (예: D:/Downloads)")
    filename: str | None = Field(None, description="저장 파일명. 미입력 시 URL에서 자동 추출")
    overwrite: bool = Field(False, description="동일 파일명 존재 시 덮어쓰기 여부")
    requester: str | None = Field(None, description="요청자 식별자 (로깅용)")
    source_page: str | None = Field(None, description="다운로드를 트리거한 페이지 URL (Referer 헤더로도 활용)")


class DirectDownloadRequest(BaseDownloadRequest):
    headers: dict[str, str] | None = Field(None, description="커스텀 HTTP 요청 헤더 (인증 토큰 등)")


class YoutubeDownloadRequest(BaseDownloadRequest):
    quality: str = Field(
        "best",
        description="해상도 프리셋: `best` | `1080p` | `720p` | `480p` | `360p` | `audio`",
    )
    audio_quality: str = Field(
        "best",
        description="오디오 품질: `best` | `high` (192k+) | `medium` (128k+) | `low` (64k+)",
    )
    subtitles: str | None = Field(
        None,
        description="자막 언어 코드. 예: `ko` | `en` | `ko,en` | `all`. 수동 자막 없으면 자동 생성 자막으로 대체",
    )
    cookies_from_browser: str | None = Field(
        None,
        description="로그인이 필요한 영상에 브라우저 쿠키 사용: `chrome` | `firefox` | `edge`",
    )
    playlist_items: str | None = Field(
        None,
        description="재생목록 다운로드 범위. 예: `1-3` | `1,3,5`",
    )


class SaveTextRequest(BaseModel):
    content: str = Field(..., description="저장할 텍스트 내용")
    directory: str = Field(..., description="저장할 로컬 디렉터리 경로 (예: D:/Downloads)")
    filename: str = Field(..., description="저장 파일명 (예: hello.txt)")
    encoding: str = Field("utf-8", description="파일 인코딩 (기본값: utf-8)")
    overwrite: bool = Field(False, description="동일 파일명 존재 시 덮어쓰기 여부")
    requester: str | None = Field(None, description="요청자 식별자 (로깅용)")


class SaveBinaryRequest(BaseModel):
    content: str = Field(..., description="저장할 바이너리 데이터 (Base64 인코딩된 문자열)")
    directory: str = Field(..., description="저장할 로컬 디렉터리 경로 (예: D:/Downloads)")
    filename: str = Field(..., description="저장 파일명 (예: image.png)")
    overwrite: bool = Field(False, description="동일 파일명 존재 시 덮어쓰기 여부")
    requester: str | None = Field(None, description="요청자 식별자 (로깅용)")


class AutoDownloadRequest(BaseDownloadRequest):
    type: str = Field(
        "auto",
        description="파일 타입: `auto` (자동 감지) | `youtube` | `video` | `image` | `file`",
    )
    quality: str = Field("best", description="해상도 프리셋 (video/youtube 타입에 적용)")
    audio_quality: str = Field("best", description="오디오 품질 (video/youtube 타입에 적용)")
    subtitles: str | None = Field(None, description="자막 언어 코드 (video/youtube 타입에 적용)")
    headers: dict[str, str] | None = Field(None, description="커스텀 HTTP 요청 헤더 (direct 타입에 적용)")
    cookies_from_browser: str | None = Field(None, description="브라우저 쿠키 사용 (video/youtube 타입에 적용)")
    playlist_items: str | None = Field(None, description="재생목록 항목 범위 (video/youtube 타입에 적용)")
