# 🎬 ASCII 비디오 터미널

비디오를 ASCII 문자로 변환하여 터미널에서 애니메이션으로 재생하는 Python 서버

## 기능

- **비디오를 ASCII 애니메이션으로 변환**: 모든 비디오 파일을 ASCII 문자 기반 애니메이션으로 변환
- **터미널에서 실시간 재생**: `curl` 명령어로 터미널에서 바로 애니메이션 감상
- **다양한 재생 옵션**: 재생 속도, 프레임 스트라이드 조절 가능
- **ANSI 컬러 지원**: 다채로운 컬러로 표현되는 ASCII 애니메이션
- **HTTP 스트리밍**: 실시간 스트리밍 방식의 부드러운 애니메이션

## 설치 및 실행

### 의존성 설치

```bash
# pip 사용 (권장)
pip install flask colorama opencv-python xtermcolor

# 또는 uv 사용
uv sync
```

### 서버 실행

```bash
python main.py
```

## 사용법

### 기본 애니메이션 감상

```bash
# 기본 애니메이션 (overdrive) 재생
curl localhost:1018

# 다른 애니메이션 재생 (soda)
curl localhost:1018/soda
```

### 재생 옵션 조절

```bash
# 재생 속도 조절 (interval: 초 단위)
curl "localhost:1018/overdrive?interval=0.2"

# 프레임 스킵 (stride: n번째 프레임마다 재생)
curl "localhost:1018/overdrive?stride=2"

# 복합 옵션
curl "localhost:1018/soda?interval=0.15&stride=3"
```

### 브라우저 접속

브라우저로 `http://localhost:1018`에 접속하면 관련 GitHub 페이지로 자동 리디렉션됩니다.

## 비디오 추가하기

### 1. 비디오 파일 준비

`videos/` 폴더에 mp4 파일을 넣어주세요:

```bash
videos/
├── overdrive.mp4
├── soda.mp4
└── your_video.mp4
```

### 2. ASCII 프레임 생성

```bash
# 예제 스크립트 수정 후 실행
python save_frames_example.py
```

`save_frames_example.py`에서 비디오 파일 경로를 수정하여 원하는 비디오를 변환할 수 있습니다.

### 3. 생성된 프레임 확인

`saved_frames/` 폴더에 ASCII 프레임 파일들이 생성됩니다:

```bash
saved_frames/
├── overdrive/
│   ├── frame_000000.txt
│   ├── frame_000001.txt
│   └── ...
└── your_video/
    ├── frame_000000.txt
    └── ...
```

## API 엔드포인트

- `GET /` - 기본 애니메이션 (overdrive) 재생
- `GET /{folder_name}` - 특정 애니메이션 재생
- `GET /health` - 서버 상태 확인

### 쿼리 파라미터

- `interval`: 프레임 간 대기 시간 (초, 기본값: 0.05)
- `stride`: 프레임 스킵 간격 (기본값: 1)

## 개발

```bash
# 개발 모드로 실행
python main.py

# 헬스 체크
curl localhost:1018/health

# 사용 가능한 애니메이션 확인
# 서버 실행 시 콘솔에 표시됩니다
```

## 기술 스택

- **Flask**: 웹 서버 프레임워크
- **OpenCV**: 비디오 처리 및 프레임 추출
- **ANSI 이스케이프 시퀀스**: 터미널 컬러 및 애니메이션
- **HTTP 스트리밍**: 실시간 애니메이션 전송

## 참고 자료

비디오를 ASCII 문자로 변환하는 코드는 [@joelibaceta/video-to-ascii](https://github.com/joelibaceta/video-to-ascii)를 사용했습니다.

## 라이선스

MIT License

---

