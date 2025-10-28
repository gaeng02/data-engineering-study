from fastapi import FastAPI, Request, Depends, HTTPException, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import Optional
import json

from database import get_db, create_tables
from models import Post, User
from auth import login_user, logout_user, get_current_user, is_logged_in
from logging_service import LoggingService
from internal_logging_service import InternalLoggingService

app = FastAPI(title="블로그 마스터 서버", description="로그인 + 블로그 + 로깅 시스템")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

create_tables()

def create_sample_data(db: Session):
    if db.query(Post).count() == 0:
        sample_posts = [
            {
                "title": "FastAPI로 웹 애플리케이션 만들기",
                "preview": "FastAPI는 현대적이고 빠른 웹 프레임워크입니다. Python 3.7+의 타입 힌트를 기반으로 하여 API를 쉽게 구축할 수 있습니다.",
                "content": """
                <h2>FastAPI 소개</h2>
                <p>FastAPI는 현대적이고 빠른 웹 프레임워크입니다. Python 3.7+의 타입 힌트를 기반으로 하여 API를 쉽게 구축할 수 있습니다.</p>
                
                <h3>주요 특징</h3>
                <ul>
                    <li><strong>빠른 성능:</strong> NodeJS와 Go와 비슷한 성능</li>
                    <li><strong>자동 문서화:</strong> Swagger UI와 ReDoc 자동 생성</li>
                    <li><strong>타입 안전성:</strong> Python 타입 힌트 기반</li>
                    <li><strong>간편한 사용:</strong> 직관적인 API 설계</li>
                </ul>
                
                <h3>설치 및 기본 사용법</h3>
                <pre><code>pip install fastapi uvicorn
# main.py
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}</code></pre>
                """,
                "author": "개발자"
            },
            {
                "title": "SQLite 데이터베이스 활용하기",
                "preview": "SQLite는 서버리스 데이터베이스로, 파일 기반으로 동작하여 개발과 테스트에 매우 유용합니다.",
                "content": """
                <h2>SQLite란?</h2>
                <p>SQLite는 서버리스 데이터베이스로, 파일 기반으로 동작하여 개발과 테스트에 매우 유용합니다.</p>
                
                <h3>장점</h3>
                <ul>
                    <li><strong>설치 불필요:</strong> 별도 서버 설치 없이 사용</li>
                    <li><strong>파일 기반:</strong> 단일 파일로 데이터베이스 관리</li>
                    <li><strong>가벼움:</strong> 최소한의 리소스 사용</li>
                    <li><strong>호환성:</strong> 다양한 프로그래밍 언어 지원</li>
                </ul>
                
                <h3>Python에서 사용하기</h3>
                <pre><code>import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# 테이블 생성
cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)''')

# 데이터 삽입
cursor.execute("INSERT INTO users (name) VALUES (?)", ("홍길동",))
conn.commit()</code></pre>
                """,
                "author": "데이터베이스 전문가"
            },
            {
                "title": "웹 애플리케이션 로깅 시스템 구축",
                "preview": "효과적인 로깅 시스템은 애플리케이션의 동작을 추적하고 문제를 해결하는 데 필수적입니다.",
                "content": """
                <h2>로깅의 중요성</h2>
                <p>효과적인 로깅 시스템은 애플리케이션의 동작을 추적하고 문제를 해결하는 데 필수적입니다.</p>
                
                <h3>로깅 레벨</h3>
                <ul>
                    <li><strong>DEBUG:</strong> 상세한 디버깅 정보</li>
                    <li><strong>INFO:</strong> 일반적인 정보</li>
                    <li><strong>WARNING:</strong> 경고 메시지</li>
                    <li><strong>ERROR:</strong> 오류 발생</li>
                    <li><strong>CRITICAL:</strong> 심각한 오류</li>
                </ul>
                
                <h3>Python 로깅 예제</h3>
                <pre><code>import logging

# 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 로그 기록
logger.info("사용자가 로그인했습니다")
logger.error("데이터베이스 연결 실패")</code></pre>
                """,
                "author": "시스템 관리자"
            },
            {
                "title": "AWS EC2에 웹 애플리케이션 배포하기",
                "preview": "AWS EC2를 사용하여 웹 애플리케이션을 클라우드에 배포하는 방법을 알아보겠습니다.",
                "content": """
                <h2>AWS EC2 배포 과정</h2>
                <p>AWS EC2를 사용하여 웹 애플리케이션을 클라우드에 배포하는 방법을 알아보겠습니다.</p>
                
                <h3>배포 단계</h3>
                <ol>
                    <li><strong>EC2 인스턴스 생성:</strong> Ubuntu 서버 선택</li>
                    <li><strong>보안 그룹 설정:</strong> 필요한 포트 열기</li>
                    <li><strong>SSH 접속:</strong> 인스턴스에 연결</li>
                    <li><strong>환경 설정:</strong> Python, 의존성 설치</li>
                    <li><strong>애플리케이션 배포:</strong> 코드 업로드 및 실행</li>
                </ol>
                
                <h3>주요 명령어</h3>
                <pre><code># 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 설치
sudo apt install python3 python3-pip -y

# 프로젝트 의존성 설치
pip3 install -r requirements.txt

# 애플리케이션 실행
uvicorn main:app --host 0.0.0.0 --port 8000</code></pre>
                """,
                "author": "DevOps 엔지니어"
            },
            {
                "title": "RESTful API 설계 원칙",
                "preview": "좋은 RESTful API를 설계하기 위한 기본 원칙과 모범 사례를 살펴보겠습니다.",
                "content": """
                <h2>RESTful API 설계 원칙</h2>
                <p>좋은 RESTful API를 설계하기 위한 기본 원칙과 모범 사례를 살펴보겠습니다.</p>
                
                <h3>REST의 핵심 원칙</h3>
                <ul>
                    <li><strong>리소스 기반:</strong> URL은 리소스를 나타냄</li>
                    <li><strong>HTTP 메서드:</strong> GET, POST, PUT, DELETE 사용</li>
                    <li><strong>상태 없음:</strong> 각 요청은 독립적</li>
                    <li><strong>계층화:</strong> 클라이언트-서버 분리</li>
                </ul>
                
                <h3>URL 설계 예제</h3>
                <pre><code>GET    /api/users          # 사용자 목록 조회
GET    /api/users/123      # 특정 사용자 조회
POST   /api/users          # 새 사용자 생성
PUT    /api/users/123      # 사용자 정보 수정
DELETE /api/users/123      # 사용자 삭제</code></pre>
                """,
                "author": "백엔드 개발자"
            },
            {
                "title": "프론트엔드와 백엔드 연동하기",
                "preview": "JavaScript를 사용하여 프론트엔드에서 백엔드 API를 호출하는 방법을 알아보겠습니다.",
                "content": """
                <h2>프론트엔드-백엔드 연동</h2>
                <p>JavaScript를 사용하여 프론트엔드에서 백엔드 API를 호출하는 방법을 알아보겠습니다.</p>
                
                <h3>Fetch API 사용</h3>
                <pre><code>// GET 요청
fetch('/api/users')
  .then(response => response.json())
  .then(data => console.log(data));

// POST 요청
fetch('/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: '홍길동',
    email: 'hong@example.com'
  })
});</code></pre>
                
                <h3>에러 처리</h3>
                <pre><code>fetch('/api/users')
  .then(response => {
    if (!response.ok) {
      throw new Error('네트워크 응답이 올바르지 않습니다');
    }
    return response.json();
  })
  .catch(error => {
    console.error('오류 발생:', error);
  });</code></pre>
                """,
                "author": "풀스택 개발자"
            }
        ]
        
        for post_data in sample_posts:
            post = Post(**post_data)
            db.add(post)
        
        db.commit()

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    create_sample_data(db)
    db.close()

def get_client_info(request: Request) -> str:
    user_agent = request.headers.get("user-agent", "")
    return user_agent

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db), session_token: Optional[str] = Cookie(None)):
    current_user = get_current_user(session_token) if session_token else None
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    logging_service = LoggingService(db)
    logging_service.log_page_view("home", 
                                 current_user["user_id"],
                                 get_client_info(request))
    
    posts = db.query(Post).order_by(Post.created_at.desc()).limit(6).all()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "posts": posts,
        "user": current_user
    })

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def post_detail(request: Request, post_id: int, db: Session = Depends(get_db), session_token: Optional[str] = Cookie(None)):
    current_user = get_current_user(session_token) if session_token else None
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    logging_service = LoggingService(db)
    logging_service.log_post_click(post_id,
                                 current_user["user_id"],
                                 get_client_info(request))
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다")
    
    other_posts = db.query(Post).filter(Post.id != post_id).order_by(Post.created_at.desc()).limit(3).all()
    
    return templates.TemplateResponse("post.html", {
        "request": request,
        "post": post,
        "user": current_user,
        "other_posts": other_posts
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    logging_service = LoggingService(db)
    logging_service.log_page_view("login", None, get_client_info(request))
    
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, nickname: str = Form(...), db: Session = Depends(get_db)):
    logging_service = LoggingService(db)
    
    user_info = login_user(db, nickname)
    if not user_info:
        raise HTTPException(status_code=400, detail="닉네임을 입력해주세요")
    
    logging_service.log_login(nickname, get_client_info(request))
    
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="session_token", value=user_info["session_token"], httponly=True)
    
    return response

@app.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db), session_token: Optional[str] = Cookie(None)):
    logging_service = LoggingService(db)
    current_user = get_current_user(session_token) if session_token else None
    
    if current_user:
        logging_service.log_logout(current_user["user_id"], get_client_info(request))
        logout_user(session_token)
    
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="session_token")
    return response

@app.post("/like/{post_id}")
async def like_post(request: Request, post_id: int, db: Session = Depends(get_db), session_token: Optional[str] = Cookie(None)):
    current_user = get_current_user(session_token) if session_token else None
    if not current_user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다")
    
    logging_service = LoggingService(db)
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다")
    
    post.likes_count += 1
    db.commit()
    
    logging_service.log_like(post_id,
                           current_user["user_id"],
                           get_client_info(request))
    
    return {"message": "좋아요가 추가되었습니다", "likes_count": post.likes_count}

@app.post("/comment/{post_id}")
async def comment_post(request: Request, post_id: int, db: Session = Depends(get_db), session_token: Optional[str] = Cookie(None)):
    current_user = get_current_user(session_token) if session_token else None
    if not current_user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다")
    
    logging_service = LoggingService(db)
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다")
    
    logging_service.log_comment_attempt(post_id,
                                       current_user["user_id"],
                                       get_client_info(request))
    
    return {"message": "댓글 시도가 기록되었습니다 (실제로는 저장되지 않음)"}

@app.get("/admin/edit/{post_id}", response_class=HTMLResponse)
async def edit_post_page(request: Request, post_id: int, db: Session = Depends(get_db), session_token: Optional[str] = Cookie(None)):
    current_user = get_current_user(session_token) if session_token else None
    if not current_user:
        return RedirectResponse(url="/login", status_code=302)
    
    if current_user["nickname"] != "gaeng02":
        raise HTTPException(status_code=403, detail="권한이 없습니다")
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다")
    
    return templates.TemplateResponse("edit_post.html", {
        "request": request,
        "post": post,
        "user": current_user
    })

@app.post("/admin/edit/{post_id}")
async def update_post(request: Request, post_id: int, db: Session = Depends(get_db), session_token: Optional[str] = Cookie(None)):
    current_user = get_current_user(session_token) if session_token else None
    if not current_user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다")
    
    if current_user["nickname"] != "gaeng02":
        raise HTTPException(status_code=403, detail="권한이 없습니다")
    
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없습니다")
    
    form_data = await request.form()
    title = form_data.get("title", "").strip()
    content = form_data.get("content", "").strip()
    preview = form_data.get("preview", "").strip()
    
    if not title or not content:
        raise HTTPException(status_code=400, detail="제목과 내용은 필수입니다")
    
    post.title = title
    post.content = content
    post.preview = preview if preview else content[:200] + "..." if len(content) > 200 else content
    
    db.commit()
    
    
    return RedirectResponse(url=f"/post/{post_id}", status_code=302)

@app.get("/logs")
async def get_logs(request: Request, caller_name: Optional[str] = None, db: Session = Depends(get_db)):
    """모든 로그 조회 API (학생 실습용)"""

    # 내부 로깅: API 호출 추적
    caller_info = {
        "ip": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown")
    }
    InternalLoggingService.log_api_call(
        endpoint="/logs",
        caller_info=caller_info,
        caller_name=caller_name
    )
    
    logging_service = LoggingService(db)
    logs = logging_service.get_all_logs()
    
    logs_data = []
    for log in logs:
        logs_data.append({
            "id": log.id,
            "user_id": log.user_id,
            "post_id": log.post_id,
            "action": log.action,
            "details": log.details,
            "user_agent": log.user_agent,
            "timestamp": log.timestamp.isoformat()
        })
    
    return logs_data

@app.get("/users")
async def get_users(request: Request, caller_name: Optional[str] = None, db: Session = Depends(get_db)):
    """모든 사용자 조회 API (학생 실습용)"""

    # 내부 로깅: API 호출 추적
    caller_info = {
        "ip": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown")
    }
    InternalLoggingService.log_api_call(
        endpoint="/users",
        caller_info=caller_info,
        caller_name=caller_name
    )
    
    users = db.query(User).order_by(User.created_at.desc()).all()
    
    users_data = []
    for user in users:
        users_data.append({
            "id": user.id,
            "nickname": user.nickname,
            "created_at": user.created_at.isoformat()
        })
    
    return users_data

if (__name__ == "__main__") :
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
