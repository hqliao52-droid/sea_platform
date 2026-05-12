from fastapi import UploadFile
from app.utils.file_utils import FileUtils

class FileService:
    """文件上传"""

    ANDROID_APK_NAME = "sea_platform_latest.apk"

    @staticmethod
    def upload_file(file: UploadFile) -> str:
        """上传文件"""
        url = FileUtils.save_file(file)

        return {"filename":file.filename,
                "url":url}
    
    @classmethod
    def get_android_download_url(cls) -> str:
        """获取 Android 下载链接"""
        return FileUtils.get_android_download_url()
    
    @classmethod
    def get_ios_download_url(cls) -> str:
        """获取 iOS 下载链接"""
        return FileUtils.get_ios_download_url()