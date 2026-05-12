from fastapi import APIRouter,UploadFile,File
from fastapi.responses import RedirectResponse
from app.services.file_service import FileService
from app.utils.result_response import Result
# from app.utils.result_response import ResultCode

router = APIRouter()

@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    result = FileService().upload_file(file)
    return Result.success(result)

@router.get("/download/android/latest")
async def get_app_download_url():
    """
    返回最新 Android APK 下载地址（JSON）
    
    返回示例：
    {
        "platform": "android",
        "version": "latest",
        "url": "https://your-domain.com/attach/apps/sea_platform_latest.apk"
    }
    """
    return FileService.get_android_download_url()


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
