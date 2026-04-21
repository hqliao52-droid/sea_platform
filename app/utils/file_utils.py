import os,uuid
from pathlib import Path
from fastapi import UploadFile
from app.config.file_config import file_config

class FileUtils:
    """文件处理"""

    @staticmethod
    def get_file_type(filename:str) -> str:
        """判断文件类型"""
        ext = filename.split(".")[-1].lower()

        if ext in ["jpg", "jpeg", "png", "gif","bmp"]:
            return "images"
        elif ext in ["mp4", "avi", "mov", "wmv"]:
            return "videos"
        elif ext in ["mp3", "wav", "ogg"]:
            return "audios"
        elif ext in ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx","txt"]:
            return "docs"
        else:
            return "others"
        
    @staticmethod
    def get_save_dir(file_type:str) -> Path:
        """获取保存目录"""
        mapping = {
            "images":file_config.IMAGE_DIR,
            "videos":file_config.VIDEO_DIR,
            "audios":file_config.AUDIO_DIR,
            "docs":file_config.DOC_DIR,
            "others":file_config.OTHER_DIR
        }
        return mapping[file_type]

    @staticmethod
    def save_file(file:UploadFile) -> str:
        """保存文件 返回访问URL"""
        file_type = FileUtils.get_file_type(file.filename)
        save_dir = FileUtils.get_save_dir(file_type)

        # 创建目录
        os.makedirs(save_dir, exist_ok=True)

        # 生成唯一文件名
        ext = file.filename.split(".")[-1]
        new_filename = f"{uuid.uuid4().hex}.{ext}"

        file_path = save_dir/new_filename

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # 返回URL
        relative_path = f"attach/{file_type}/{new_filename}"
        url = f"{file_config.FILE_HOST}/{relative_path}"

        return url
