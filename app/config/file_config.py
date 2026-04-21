from pathlib import Path
from app.config.settings import settings

class FileConfig:
    """文件上传配置"""
    # 项目根目录（sea_ai_platform）
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # 附件目录
    ATTACH_DIR = BASE_DIR / "attach"

    # 分类目录
    IMAGE_DIR = ATTACH_DIR / "images"
    DOC_DIR = ATTACH_DIR / "docs"
    VIDEO_DIR = ATTACH_DIR / "videos"
    AUDIO_DIR = ATTACH_DIR / "audios"
    OTHER_DIR = ATTACH_DIR / "others"

    # 访问host(生产环境需改为nginx域名)
    FILE_HOST = f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}"

file_config = FileConfig()  