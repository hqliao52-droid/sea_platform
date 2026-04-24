from app.utils.logger import Logger
from app.models.llm_api_log import LlmApiLog
from app.crud.data_crud.llm_api_log import LlmApiLogCRUD
from app.config.mysql_config import db_session
from typing import List

class LlmApiLogOperator:
    """LLM API 调用日志记录"""
    def __init__(self):
        self.logger = Logger.setup_logger(Logger.set_file_date())
        self.llm_api_log_curd = LlmApiLogCRUD()

    def get_info_by_id(self,id:int) -> LlmApiLog:
        db = db_session()
        try:
            result = self.llm_api_log_curd.get_llm_api_log_by_id(db,id)
            self.logger.info(f"查询成功:{result}")
            return result
        except Exception as e:
            self.logger.error(f"查询失败:{e}")
            return None
        finally:
            db.close()
    
    def get_info_by_message_id(self,message_id:int) -> LlmApiLog:
        db = db_session()
        try:
            result = self.llm_api_log_curd.get_llm_api_log_by_message_id(db,message_id)
            self.logger.info(f"查询成功:{result}")
            return result
        except Exception as e:
            self.logger.error(f"查询失败:{e}")
            return None
        finally:
            db.close()
    
    def get_info_by_model_name(self,model_name:str) -> List[LlmApiLog]:
        db = db_session()
        try:
            result = self.llm_api_log_curd.get_llm_api_log_by_model_name(db,model_name)
            self.logger.info(f"查询成功:{result}")
            return result
        except Exception as e:
            self.logger.error(f"查询失败:{e}")
            return None
        finally:
            db.close()


