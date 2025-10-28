"""
SQLAlchemy 데이터베이스 모델 정의
User, Post, Log 모델 포함
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    """
    사용자 모델 - 닉네임 기반 간단 로그인
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정
    logs = relationship("Log", back_populates="user")

class Post(Base):
    """
    블로그 포스트 모델
    """
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    preview = Column(String(500), nullable=False)  # 미리보기용 요약
    author = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    likes_count = Column(Integer, default=0)
    
    # 관계 설정
    logs = relationship("Log", back_populates="post")

class Log (Base) :

    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # 로그인하지 않은 사용자도 로깅
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)  # 포스트와 관련 없는 액션도 있음
    action = Column(String(50), nullable=False)  # login, logout, page_view, post_click, like, comment_attempt 등
    details = Column(Text, nullable=True)  # 추가 세부 정보 (JSON 형태로 저장 가능)
    user_agent = Column(Text, nullable=True)  # 브라우저 정보
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정
    user = relationship("User", back_populates="logs")
    post = relationship("Post", back_populates="logs")
