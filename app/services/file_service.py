from fastapi import UploadFile
from pathlib import Path
from app.utils.file_utils import FileUtils
from app.utils.qrcode_utils import QRCodeUtils

class FileService:
    """文件上传"""

    ANDROID_APK_NAME = "sea_platform_latest.apk"

    @staticmethod
    async def upload_file(file: UploadFile) -> str:
        """上传文件"""
        url = await FileUtils.save_file(file)

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
    
    @classmethod
    async def android_generate_qrcode(cls) -> str:
        """
        如果二维码已存在，则直接返回；
        不存在时才生成。
        """
        path = "attach/images/android_qrcode.png"
        save_path = Path(path)

        if not save_path.exists():
            download_url = cls.get_android_download_url()
            await QRCodeUtils.generate_qrcode(download_url, save_path)
        
        return FileUtils.get_android_rqcode()


    @classmethod
    async def ios_generate_qrcode(cls) -> str:
        """生成二维码"""
        path = "attach/images/ios_qrcode.png"
        save_path = Path(path)

        if not save_path.exists():
            download_url = cls.get_ios_download_url()
            await QRCodeUtils.generate_qrcode(download_url, save_path)

        return FileUtils.get_ios_rqcode()
    