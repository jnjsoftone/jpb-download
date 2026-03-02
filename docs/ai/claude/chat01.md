"""
C:\JnJ\Developments\Projects\@chrome-extension\_backend\python 를 참고하여 file-downloader 를 생성해주세요.
"""


● 완료했습니다. 생성된 구조:

  file-downloader/
  ├── pyproject.toml      # uv 의존성 (fastapi, uvicorn, yt-dlp, requests, python-multipart)
  ├── uv.lock
  ├── main.py             # FastAPI 앱, POST /download 엔드포인트
  ├── downloader.py       # 타입 감지 + 분기 로직
  └── utils.py            # ensure_directory 헬퍼

  서버 실행:
  cd file-downloader
  uv run uvicorn main:app --reload

  Chrome Extension에서 호출 예시:
  await fetch("http://127.0.0.1:8000/download", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-token": "my-secret"
    },
    body: JSON.stringify({
      url: "https://youtube.com/watch?v=...",
      directory: "D:/Downloads",
      type: "auto"
    })
  });

  참고: main.py의 SECRET_TOKEN = "my-secret" 값은 실제 사용 전에 변경하세요.


===============

{
    "status": "success",
    "detail": {
        "yt_dlp_output": "[youtube] Extracting URL: https://www.youtube.com/watch?v=oW2nLWGnqHg&t=19s\n[youtube] oW2nLWGnqHg: Downloading webpage\n[youtube] oW2nLWGnqHg: Downloading android vr player API JSON\n[info] oW2nLWGnqHg: Downloading 1 format(s): 137+251\n[download] Destination: D:\\Downloads\\가진돈 잘쓰는 기업에 투자하자 ‘자산회전율’ 팩터 [퀀트 팩터 가이드 EP.25] [oW2nLWGnqHg].f137.mp4\n\n[download]   0.0% of   22.40MiB at  474.04KiB/s ETA 00:48\n[download]   0.0% of   22.40MiB at    1.03MiB/s ETA 00:21\n[download]   0.0% of   22.40MiB at    2.02MiB/s ETA 00:11\n[download]   0.1% of   22.40MiB at    3.41MiB/s ETA 00:06\n[download]   0.1% of   22.40MiB at    6.04MiB/s ETA 00:03\n[download]   0.3% of   22.40MiB at   10.93MiB/s ETA 00:02\n[download]   0.6% of   22.40MiB at   19.11MiB/s ETA 00:01\n[download]   1.1% of   22.40MiB at   19.94MiB/s ETA 00:01\n[download]   2.2% of   22.40MiB at   16.84MiB/s ETA 00:01\n[download]   4.5% of   22.40MiB at   15.68MiB/s ETA 00:01\n[download]   8.9% of   22.40MiB at   15.23MiB/s ETA 00:01\n[download]  17.9% of   22.40MiB at    2.72MiB/s ETA 00:06\n[download]  24.5% of   22.40MiB at    3.18MiB/s ETA 00:05\n[download]  37.9% of   22.40MiB at    2.61MiB/s ETA 00:05\n[download]  43.2% of   22.40MiB at    2.90MiB/s ETA 00:04\n[download]  43.2% of   22.40MiB at  Unknown B/s ETA Unknown\n[download]  43.2% of   22.40MiB at    2.67MiB/s ETA 00:04  \n[download]  43.2% of   22.40MiB at    4.51MiB/s ETA 00:02\n[download]  43.2% of   22.40MiB at    7.43MiB/s ETA 00:01\n[download]  43.3% of   22.40MiB at   12.16MiB/s ETA 00:01\n[download]  43.4% of   22.40MiB at   19.79MiB/s ETA 00:00\n[download]  43.7% of   22.40MiB at   32.29MiB/s ETA 00:00\n[download]  44.3% of   22.40MiB at   30.53MiB/s ETA 00:00\n[download]  45.4% of   22.40MiB at  624.39KiB/s ETA 00:20\n[download]  46.8% of   22.40MiB at  987.41KiB/s ETA 00:12\n[download]  49.5% of   22.40MiB at    1.62MiB/s ETA 00:06\n[download]  55.0% of   22.40MiB at    1.64MiB/s ETA 00:06\n[download]  62.4% of   22.40MiB at    2.49MiB/s ETA 00:03\n[download]  77.3% of   22.40MiB at    2.34MiB/s ETA 00:02\n[download]  86.9% of   22.40MiB at    2.44MiB/s ETA 00:01\n[download]  87.7% of   22.40MiB at    2.48MiB/s ETA 00:01\n[download]  87.8% of   22.40MiB at  Unknown B/s ETA Unknown\n[download]  87.8% of   22.40MiB at  Unknown B/s ETA Unknown\n[download]  87.8% of   22.40MiB at  Unknown B/s ETA Unknown\n[download]  87.8% of   22.40MiB at   10.41MiB/s ETA 00:00  \n[download]  87.9% of   22.40MiB at   15.39MiB/s ETA 00:00\n[download]  88.0% of   22.40MiB at   20.26MiB/s ETA 00:00\n[download]  88.3% of   22.40MiB at   31.32MiB/s ETA 00:00\n[download]  88.9% of   22.40MiB at   20.58MiB/s ETA 00:00\n[download]  90.0% of   22.40MiB at  587.98KiB/s ETA 00:03\n[download]  91.3% of   22.40MiB at  909.30KiB/s ETA 00:02\n[download]  93.9% of   22.40MiB at    1.48MiB/s ETA 00:00\n[download]  99.1% of   22.40MiB at    1.52MiB/s ETA 00:00\n[download] 100.0% of   22.40MiB at    1.63MiB/s ETA 00:00\n[download] 100% of   22.40MiB in 00:00:10 at 2.11MiB/s   \n[download] Destination: D:\\Downloads\\가진돈 잘쓰는 기업에 투자하자 ‘자산회전율’ 팩터 [퀀트 팩터 가이드 EP.25] [oW2nLWGnqHg].f251.webm\n\n[download]   0.0% of    5.21MiB at  Unknown B/s ETA Unknown\n[download]   0.1% of    5.21MiB at    2.40MiB/s ETA 00:02  \n[download]   0.1% of    5.21MiB at    4.28MiB/s ETA 00:01\n[download]   0.3% of    5.21MiB at    5.72MiB/s ETA 00:00\n[download]   0.6% of    5.21MiB at    9.65MiB/s ETA 00:00\n[download]   1.2% of    5.21MiB at   13.22MiB/s ETA 00:00\n[download]   2.4% of    5.21MiB at   22.03MiB/s ETA 00:00\n[download]   4.8% of    5.21MiB at   20.16MiB/s ETA 00:00\n[download]   9.6% of    5.21MiB at   27.98MiB/s ETA 00:00\n[download]  19.2% of    5.21MiB at   37.58MiB/s ETA 00:00\n[download]  38.4% of    5.21MiB at   45.02MiB/s ETA 00:00\n[download]  76.8% of    5.21MiB at    4.28MiB/s ETA 00:00\n[download] 100.0% of    5.21MiB at    5.42MiB/s ETA 00:00\n[download] 100% of    5.21MiB in 00:00:00 at 5.36MiB/s   \n"
    }
}