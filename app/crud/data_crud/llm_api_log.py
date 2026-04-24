from app.crud.sea_data_base import BaseCRUD
from app.models.llm_api_log import LlmApiLog
from sqlalchemy.orm import Session
from typing import List

class LlmApiLogCRUD(BaseCRUD):
    def __init__(self):
        super().__init__(LlmApiLog)
    
    def get_llm_api_log_by_id(self,db:Session,id:int) -> LlmApiLog:
        return db.query(LlmApiLog).filter(LlmApiLog.id == id).first()
    
    def get_llm_api_log_by_session_id(self,db:Session,session_id:int) -> List[LlmApiLog]:
        return db.query(LlmApiLog).filter(LlmApiLog.session_id == session_id).all()
    
    def get_llm_api_log_by_message_id(self,db:Session,message_id:int) -> LlmApiLog:
        return db.query(LlmApiLog).filter(LlmApiLog.message_id == message_id).first()
    
    def get_llm_api_log_by_model_name(self,db:Session,model_name:str) -> List[LlmApiLog]:
        return db.query(LlmApiLog).filter(LlmApiLog.model_name == model_name).all()
