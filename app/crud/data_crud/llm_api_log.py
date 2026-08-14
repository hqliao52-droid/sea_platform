from app.crud.sea_data_base import BaseCRUD
from app.models.llm_api_log import LlmApiLog
from sqlalchemy.orm import Session
from typing import List

class LlmApiLogCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(LlmApiLog)
    
    async def get_llm_api_log_by_id(self,db:Session,id:int) -> LlmApiLog:
        return await db.query(LlmApiLog).filter(LlmApiLog.id == id).first()
    
    async def get_llm_api_log_by_session_id(self,db:Session,session_id:int) -> List[LlmApiLog]:
        return await db.query(LlmApiLog).filter(LlmApiLog.session_id == session_id).all()
    
    async def get_llm_api_log_by_message_id(self,db:Session,message_id:int) -> LlmApiLog:
        return await db.query(LlmApiLog).filter(LlmApiLog.message_id == message_id).first()
    
    async def get_llm_api_log_by_model_name(self,db:Session,model_name:str) -> List[LlmApiLog]:
        return await db.query(LlmApiLog).filter(LlmApiLog.model_name == model_name).all()
