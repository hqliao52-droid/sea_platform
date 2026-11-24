from fastapi import UploadFile
from pathlib import Path

from app.utils.file_utils import FileUtils
from app.utils.qrcode_utils import QRCodeUtils
from app.utils.log import logger

class FileService:
    """文件上传"""

    ANDROID_APK_NAME = "sea_platform_latest.apk"

    @staticmethod
    async def upload_file(file: UploadFile) -> dict:
        """上传文件"""
        try:
            url = await FileUtils.save_file(file)
        except Exception as e:
            # 用 opt(exception=True) 而不是 logger.error(e)：
            # 前者保留完整堆栈，后者只剩一行错误字符串，线上根本定位不到位置
            logger.opt(exception=True).error(
                "保存文件失败 | filename={!r} | content_type={}",
                file.filename,
                file.content_type,
            )
            return {"filename": None, "url": None, "message": str(e) or "上传失败"}
        return {"filename": file.filename, "url": url}

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
