import time

from fastapi import APIRouter, UploadFile, File, Depends

from app.services.file_service import FileService
from app.models.user_model import UserModel
from app.utils.result_response import Result
from app.utils.result_response import ResultCode
from app.utils.log import logger
from app.core.user_deps import get_current_user

router = APIRouter()


@router.post("/upload_file")
async def upload_file(
    file: UploadFile = File(...),
    user_info: UserModel = Depends(get_current_user),
):
    # filename 用 {!r} 输出，避免文件名里的换行符伪造日志行
    logger.info(
        "上传开始 | user={} | filename={!r} | content_type={}",
        user_info.username,
        file.filename,
        file.content_type,
    )

    start = time.perf_counter()
    result = await FileService().upload_file(file)
    cost_ms = (time.perf_counter() - start) * 1000

    # FileService 内部会把异常吞成 {"url": None, "message": ...} 并原样返回，
    # 这里必须显式把失败打成 WARNING，否则接口看起来永远是成功的
    if not result.get("url"):
        logger.warning(
            "上传失败 | user={} | filename={!r} | 耗时 {:.1f}ms | reason={}",
            user_info.username,
            file.filename,
            cost_ms,
            result.get("message"),
        )
    else:
        logger.info(
            "上传完成 | user={} | filename={!r} | 耗时 {:.1f}ms | url={}",
            user_info.username,
            file.filename,
            cost_ms,
            result.get("url"),
        )
    return Result.success(result)


@router.get("/download/app/latest")
async def get_app_download_url():
    """
    返回最新 APK 下载地址（JSON）
    """
    android_file = None
    android_qrcode = None
    try:
        android_file = FileService.get_android_download_url()
        android_qrcode = await FileService.android_generate_qrcode()
    except Exception as e:
        return Result.error(
            ResultCode.FILE_NOT_FOUND, msg=f"Android安装部未找到{str(e)}"
        )

    ios = None
    ios_qrcode = None
    try:
        ios = FileService.get_ios_download_url()
        ios_qrcode = await FileService.ios_generate_qrcode()
    except Exception as e:
        return Result.error(ResultCode.FILE_NOT_FOUND, msg=f"IOS安装包未找到{str(e)}")
    android_url = {
        "platform": "android",
        "version": "latest",
        "url": android_file,
        "qrcode": android_qrcode,
    }
    ios_url = {"platform": "ios", "version": "latest", "url": ios, "qrcode": ios_qrcode}
    result = {"android": android_url, "ios": ios_url}
    return Result.success(result)


# @router.get("/download/android")
# async def download_android():
#     """
#     Android 下载接口（直接跳转到 APK 文件）

#     用户访问：
#         /file/download/android

#     浏览器会自动跳转到：
#         /attach/apps/sea_platform_latest.apk
#     """
#     url = FileService.get_android_download_url()
#     return RedirectResponse(url=url)
