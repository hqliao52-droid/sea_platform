from app.crud.sea_data_base import BaseCRUD
from app.models.chat_session import ChatSession
from sqlalchemy.orm import Session
from typing import List

class ChatSessionCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(ChatSession)
    
    def get_chat_session_by_id(self,db:Session,id:int) -> ChatSession:
        return db.query(ChatSession).filter(ChatSession.id == id).first()
    
    def get_chat_session_by_user_id(self,db:Session,user_id:int) -> List[ChatSession]:
        return db.query(ChatSession).filter(ChatSession.user_id == user_id).order_by(ChatSession.update_time.desc()).all()
    
    def get_chat_session_by_llm_id(self,db:Session,llm_id:int) -> List[ChatSession]:
        return db.query(ChatSession).filter(ChatSession.llm_id == llm_id).order_by(ChatSession.update_time.desc()).all()
    