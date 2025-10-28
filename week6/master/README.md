# FastAPI 마스터 서버
## 로그인 + 블로그 + 로깅 시스템

### 📋 프로젝트 개요
FastAPI로 구현된 마스터 서버로, 닉네임 기반 간단 로그인과 블로그 기능을 제공하며 모든 사용자 상호작용을 로깅합니다.

### 🏗️ 프로젝트 구조
```
week6/
├── main.py              # FastAPI 메인 애플리케이션
├── database.py          # SQLite 데이터베이스 설정
├── models.py            # SQLAlchemy 모델 정의 (User, Post, Log)
├── auth.py              # 닉네임 기반 인증 시스템
├── logging_service.py   # 모든 상호작용 로깅 서비스
├── requirements.txt     # Python 의존성
├── README.md           # 실행 및 배포 가이드
├── templates/          # HTML 템플릿
│   ├── base.html       # 기본 레이아웃
│   ├── index.html      # 홈 페이지 (포스트 미리보기)
│   ├── post.html       # 포스트 상세 페이지
│   └── login.html      # 로그인 페이지
└── static/             # CSS, JS 파일
    ├── style.css       # 스타일시트
    └── script.js       # JavaScript 기능
```

### ✨ 주요 기능
- **간단 로그인**: 닉네임만 입력하면 자동 계정 생성 및 로그인
- **인증 기반 접근**: 로그인하지 않으면 모든 페이지 접근 차단
- **블로그 시스템**: 6개 포스트 미리보기 카드, 상세 페이지
- **어드민 기능**: 관리자는 게시글 수정 가능
- **상호작용 로깅**: 모든 사용자 행동을 데이터베이스에 기록
- **로그 API**: `GET /logs` 엔드포인트로 누적 로그 조회

### 📊 로깅 시스템

#### 기록되는 액션들
- `login`: 사용자 로그인
- `logout`: 사용자 로그아웃  
- `page_view`: 페이지 방문
- `post_click`: 포스트 클릭
- `like`: 좋아요 클릭
- `comment_attempt`: 댓글 시도
- `post_edit`: 게시글 수정 (관리자만)

#### 로그 조회 방법
```bash
# 3. Python requests 사용
import requests
response = requests.get('http://43.200.129.41:8000/logs', params={'caller_name': '홍길동'})
logs = response.json()
```

#### 로그 API 응답 예시
```json
[
  {
    "id": 1,
    "user_id": 1,
    "post_id": null,
    "action": "login",
    "details": "User ID 1 logged in",
    "user_agent": "Mozilla/5.0...",
    "timestamp": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "user_id": 1,
    "post_id": 1,
    "action": "post_click",
    "details": "Clicked on post 1",
    "user_agent": "Mozilla/5.0...",
    "timestamp": "2024-01-15T10:35:00"
  }
]
```

#### 사용자 API 응답 예시
```json
[
  {
    "id": 1,
    "nickname": "testuser",
    "created_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "nickname": "gaeng02",
    "created_at": "2024-01-15T10:35:00"
  }
]
```


### 📝 API 엔드포인트

| 메서드 | 경로 | 설명 | 인증 필요 |
|--------|------|------|-----------|
| GET | `/` | 홈 페이지 (포스트 미리보기) | ✅ |
| GET | `/post/{id}` | 포스트 상세 페이지 | ✅ |
| GET | `/login` | 로그인 페이지 | ❌ |
| POST | `/login` | 로그인 처리 | ❌ |
| POST | `/logout` | 로그아웃 처리 | ✅ |
| POST | `/like/{id}` | 포스트 좋아요 | ✅ |
| POST | `/comment/{id}` | 댓글 시도 | ✅ |
| GET | `/admin/edit/{id}` | 게시글 수정 페이지 | ✅ (관리자만) |
| POST | `/admin/edit/{id}` | 게시글 수정 처리 | ✅ (관리자만) |
| GET | `/logs` | 모든 로그 조회 (JSON) | ❌ |
| GET | `/users` | 모든 사용자 조회 (JSON) | ❌ |

### 🎯 학습 목표 달성
- ✅ FastAPI 기본 구조 이해
- ✅ SQLite 데이터베이스 연동
- ✅ 템플릿 엔진 (Jinja2) 사용
- ✅ 사용자 인증 시스템 구현
- ✅ 로깅 시스템 구축
- ✅ AWS EC2 배포 경험
- ✅ RESTful API 설계
