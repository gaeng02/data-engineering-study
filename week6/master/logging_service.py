from sqlalchemy.orm import Session
from models import Log, User, Post
from datetime import datetime
from typing import Optional
import json

class LoggingService :
    def __init__(self, db: Session) :
        self.db = db
    
    def log_action (
        self,
        action: str,
        user_id: Optional[int] = None,
        post_id: Optional[int] = None,
        details: Optional[str] = None,
        user_agent: Optional[str] = None
    ) :
        log_entry = Log(
            user_id=user_id,
            post_id=post_id,
            action=action,
            details=details,
            user_agent=user_agent,
            timestamp=datetime.utcnow()
        )
        
        self.db.add(log_entry)
        self.db.commit()
    
    def log_login (self, nickname: str, user_agent: str = None) : 
        user = self.db.query(User).filter(User.nickname == nickname).first()
        if not user :
            user = User(nickname=nickname)
            self.db.add(user)
            self.db.commit()
        
        self.log_action(
            action="login",
            user_id=user.id,
            details=f"User ID {user.id} logged in",
            user_agent=user_agent
        )
        return user
    
    def log_logout(self, user_id: int, user_agent: str = None):
        self.log_action(
            action="logout",
            user_id=user_id,
            details=f"User ID {user_id} logged out",
            user_agent=user_agent
        )
    
    def log_page_view(self, page: str, user_id: int = None, user_agent: str = None):
        self.log_action(
            action="page_view",
            user_id=user_id,
            details=f"Viewed page: {page}",
            user_agent=user_agent
        )
    
    def log_post_click(self, post_id: int, user_id: int = None, user_agent: str = None):
        self.log_action(
            action="post_click",
            user_id=user_id,
            post_id=post_id,
            details=f"Clicked on post {post_id}",
            user_agent=user_agent
        )
    
    def log_like(self, post_id: int, user_id: int = None, user_agent: str = None):
        self.log_action(
            action="like",
            user_id=user_id,
            post_id=post_id,
            details=f"Liked post {post_id}",
            user_agent=user_agent
        )
    
    def log_comment_attempt(self, post_id: int, user_id: int = None, user_agent: str = None):
        self.log_action(
            action="comment_attempt",
            user_id=user_id,
            post_id=post_id,
            details=f"Attempted to comment on post {post_id}",
            user_agent=user_agent
        )
    
    def get_all_logs(self):
        logs = self.db.query(Log).order_by(Log.timestamp.desc()).all()
        return logs
