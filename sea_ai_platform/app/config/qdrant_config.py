"""
Qdrant 核心配置文件
统一管理连接信息、向量模型、集合命名规则
支持后续扩展多集合配置
"""
from app.config.settings import settings

class QdrantConfig:
    # 服务连接配置
    HOST = settings.QDRANT_HOST
    PORT = settings.QDRANT_PORT
    API_KEY = settings.QDRANT_API_KEY

    # 向量距离算法
    DISTANCE_TYPE = "COSINE"

    # 向量模型与嵌入函数
    # @staticmethod
    # def get_embedding_function():
    #     """根据配置自动选择嵌入模型函数"""
    #     if MODEL_PATH == global_models.embedding_model_bge_large:
    #         return embed_bgr_large
    #     return embed

    @staticmethod
    def get_news_details_collection_name(vector_dim: int) -> str:
        """统一集合命名规则：支持后续扩展其他集合"""
        return f"news_details_{vector_dim}"

    # @staticmethod
    # def get_collection_name(vector_dim: int) -> str:
    #     return f"_{vector_dim}"
