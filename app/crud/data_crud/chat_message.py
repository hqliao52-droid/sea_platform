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
    
    def get_chat_message_by_pre_id(self,db:Session,pre_id:int) -> ChatMessage:
        return db.query(ChatMessage).filter(ChatMessage.pre_id == pre_id).first()

    def get_dialog_history(self,db:Session,user_id:int,session_id:int,current_id:int) -> List[ChatMessage]:
       return db.query(ChatMessage.id,ChatMessage.role,ChatMessage.content,ChatMessage.llm_refer_data,ChatMessage.llm_refer_data_id)\
        .filter(
            ChatMessage.id < current_id,
            ChatMessage.user_id == user_id,
            ChatMessage.session_id == session_id,
            ChatMessage.is_deleted == 0,
            ChatMessage.status == 'done'
        )\
        .order_by(ChatMessage.id.desc())\
        .limit(6)\
        .all()
    