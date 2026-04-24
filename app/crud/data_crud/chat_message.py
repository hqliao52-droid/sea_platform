from app.crud.sea_data_base import BaseCRUD
from app.models.chat_message import ChatMessage
from sqlalchemy.orm import Session
from typing import List

class ChatMessageCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(ChatMessage)

    def get_chat_message_by_id(self,db:Session,id:int) -> ChatMessage:
        return db.query(ChatMessage).filter(ChatMessage.id == id).first()
    
    def get_chat_message_by_user_id(self,db:Session,user_id:int) -> List[ChatMessage]:
        return db.query(ChatMessage).filter(ChatMessage.user_id == user_id).all()
    
    def get_chat_message_by_session_id(self,db:Session,session_id:int) -> List[ChatMessage]:
        return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).all()
    