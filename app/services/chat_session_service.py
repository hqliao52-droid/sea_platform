from app.utils.logger import Logger
from app.models.chat_session import ChatSession
from app.schemas.chat_session.chat_session import ChatSessionSchema
from app.crud.data_crud.chat_session import ChatSessionCRUD
from app.config.mysql_config import db_session
from typing import List

class ChatSessionOperator:
    """会话窗口操作类"""

    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.chat_session_curd = ChatSessionCRUD()
    
    def get_chat_session_by_id(self,id:int) -> ChatSessionSchema:
        db = db_session()
        try:
            chat_session = self.chat_session_curd.get(db,id)
            chat_session_result = ChatSessionSchema.from_orm(chat_session)
            return chat_session_result
        except Exception as e:
            self.logger.error(e)
            return None
        finally:
            db.close()

    def get_chat_session_by_llm_id(self,llm_id:int) -> List[ChatSessionSchema]:
        db = db_session()
        try:
            chat_session = self.chat_session_curd.get_chat_session_by_llm_id(db,llm_id)
            chat_session_result = [ChatSessionSchema.from_orm(item) for item in chat_session]
            return chat_session_result
        except Exception as e:
            self.logger.error(e)
            return None
        finally:
            db.close()

    def get_chat_session_by_user_id(self,user_id:int) -> List[ChatSessionSchema]:
        db = db_session()
        try:
            chat_session = self.chat_session_curd.get_chat_session_by_user_id(db,user_id)
            chat_session_result = [ChatSessionSchema.from_orm(item) for item in chat_session]
            return chat_session_result
        except Exception as e:
            self.logger.error(e)
            return None
        finally:
            db.close()

    def new_session(self,user_id:int) -> ChatSessionSchema:
        db = db_session()
        try:
            new_session = ChatSession(user_id=user_id,llm_id=1,session_topic="新会话")
            chat_session_result = self.chat_session_curd.insert(db,new_session)
            self.logger.info(f"新的会话创建成功：{chat_session_result}")
            return ChatSessionSchema.from_orm(chat_session_result)
        except Exception as e:
            self.logger.error(e)
            return None
        finally:
            db.close()
            
            
            

        