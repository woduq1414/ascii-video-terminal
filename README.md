# 🐦 ASCII Terminal Parrot

Python implementation of [parrot.live](https://github.com/hugomd/parrot.live) - bringing animated parrots to terminals everywhere!

## 기능

- `curl` 명령어로 터미널에서 애니메이션 앵무새 감상
- 브라우저 접속 시 자동으로 원본 GitHub 페이지로 리디렉션
- ANSI 컬러 코드를 사용한 다채로운 애니메이션
- 스트리밍 방식의 실시간 애니메이션

## 사용법

### 서버 실행

```bash
# 의존성 설치
pip install flask colorama

# 서버 시작
python main.py
```

### 애니메이션 감상

```bash
# 터미널에서 앵무새 애니메이션 보기
curl localhost:8080

# 또는 원본 parrot.live 스타일로
curl parrot.live
```

### 브라우저에서

브라우저로 `http://localhost:8080`에 접속하면 자동으로 원본 parrot.live GitHub 페이지로 리디렉션됩니다.

## 개발

```bash
# 개발 모드로 실행
python main.py

# 헬스 체크
curl localhost:8080/health
```

## 원본 프로젝트

이 프로젝트는 [hugomd/parrot.live](https://github.com/hugomd/parrot.live)의 Python 구현 버전입니다.

## 기술 스택

- **Flask**: 웹 서버 프레임워크
- **ANSI 이스케이프 시퀀스**: 터미널 컬러 및 애니메이션
- **HTTP 스트리밍**: 실시간 애니메이션 전송

## 라이선스

원본 프로젝트와 동일한 오픈소스 라이선스를 따릅니다.

---

🎉 **Party Parrot이 당신의 터미널을 찾아갑니다!** 🎉
