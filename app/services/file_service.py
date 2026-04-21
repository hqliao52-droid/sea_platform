from fastapi import UploadFile
from app.utils.file_utils import FileUtils

class FileService:
    """文件上传"""

    @staticmethod
    def upload_file(file: UploadFile) -> str:
        """上传文件"""
        url = FileUtils.save_file(file)

        return {"filename":file.filename,
                "url":url}