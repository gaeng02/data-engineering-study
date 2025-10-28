from sqlalchemy.orm import Session
from models import User
from typing import Optional
import secrets

active_sessions = {}

def create_session_token() -> str:
    return secrets.token_urlsafe(32)

def login_user(db: Session, nickname: str) -> Optional[dict]:
    if not nickname or len(nickname.strip()) == 0:
        return None
    
    nickname = nickname.strip()
    
    user = db.query(User).filter(User.nickname == nickname).first()
    if not user:
        user = User(nickname=nickname)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    session_token = create_session_token()
    active_sessions[session_token] = {
        "user_id": user.id,
        "nickname": user.nickname,
        "login_time": user.created_at
    }
    
    return {
        "user_id": user.id,
        "nickname": user.nickname,
        "session_token": session_token
    }

def logout_user(session_token: str) -> bool :
    if session_token in active_sessions:
        del active_sessions[session_token]
        return True
    return False

def get_current_user(session_token: str) -> Optional[dict] :
    return active_sessions.get(session_token)

def is_logged_in(session_token: str) -> bool :
    return session_token in active_sessions
