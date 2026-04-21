from fastapi import APIRouter,UploadFile,File
from app.services.file_service import FileService
from app.utils.result_response import Result
# from app.utils.result_response import ResultCode

router = APIRouter()

@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    result = FileService().upload_file(file)
    return Result.success(result)