import os
import uuid
import aiofiles
from pathlib import Path

from fastapi import UploadFile
from contextlib import suppress

from app.config.file_config import file_config
from app.config.settings import settings
from app.utils.log import logger


class FileUtils:
    """文件处理"""

    @staticmethod
    def get_file_type(filename: str) -> str:
        """判断文件类型"""
        ext = filename.split(".")[-1].lower()

        if ext in ["jpg", "jpeg", "png", "gif", "bmp"]:
            return "images"
        elif ext in ["mp4", "avi", "mov", "wmv"]:
            return "videos"
        elif ext in ["mp3", "wav", "ogg"]:
            return "audios"
        elif ext in ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt"]:
            return "docs"
        elif ext in ["apk", "ipa"]:
            return "apps"
        else:
            return "others"

    @staticmethod
    def get_save_dir(file_type: str) -> Path:
        """获取保存目录"""
        mapping = {
            "images": file_config.IMAGE_DIR,
            "videos": file_config.VIDEO_DIR,
            "audios": file_config.AUDIO_DIR,
            "docs": file_config.DOC_DIR,
            "others": file_config.OTHER_DIR,
        }
        return mapping[file_type]

    @staticmethod
    async def save_file(file: UploadFile) -> str:
        file_type = FileUtils.get_file_type(file.filename)
        logger.debug(
            "文件类型判定 | filename={!r} | type={}", file.filename, file_type
        )
        save_dir = FileUtils.get_save_dir(file_type)
        os.makedirs(save_dir, exist_ok=True)

        ext = Path(file.filename).suffix
        new_filename = f"{uuid.uuid4().hex}{ext}"
        file_path = save_dir / new_filename

        total = 0
        try:
            async with aiofiles.open(file_path, "wb") as out:
                # 用 UploadFile.read 的异步接口 + 分块，避免整文件入内存
                while chunk := await file.read(1024 * 1024):
                    await out.write(chunk)
                    total += len(chunk)
        except Exception:
            with suppress(FileNotFoundError):
                file_path.unlink()
            logger.opt(exception=True).error(
                "写入文件失败 | path={} | 已写入 {} bytes", file_path, total
            )
            raise

        logger.debug("文件写入完成 | path={} | size={} bytes", file_path, total)

        relative_path = f"attach/{file_type}/{new_filename}"
        return f"{file_config.FILE_HOST}/{relative_path}"

    @staticmethod
    def get_android_download_url() -> str:
        """获取 Android APK 下载地址"""
        # return f"{file_config.FILE_HOST}/attach/apps/{file_config.ANDROID_APK_NAME}"
        return settings.APK_PATH

    @staticmethod
    def get_ios_download_url() -> str:
        """获取 ios APK 下载地址"""
        return f"{file_config.FILE_HOST}/attach/apps/{file_config.IOS_APK_NAME}"

    @staticmethod
    def get_android_rqcode() -> str:
        """获取 APP 二维码"""
        return f"{file_config.FILE_HOST}/attach/images/android_qrcode.png"

    @staticmethod
    def get_ios_rqcode() -> str:
        """获取 APP 二维码"""
        return f"{file_config.FILE_HOST}/attach/images/ios_qrcode.png"
