from fastapi import APIRouter, UploadFile, File
import os
import hashlib
from datetime import datetime
from common.utils import ApiResponse
import aiofiles

router = APIRouter(prefix='/common')

# 通过文件上传/下载
@router.post("/upload")
async def upload(files: list[UploadFile] = File(...)):
    if not files:
        return ApiResponse.error(message="没有文件上传")

    os.makedirs("upload/files", exist_ok=True)
    filenames = []

    for file in files:
        original_name = file.filename or "unknown"
        name, extension = os.path.splitext(original_name)


        # 异步读取文件内容
        content = await file.read()

        # 计算MD5,取前8位
        file_md5 = hashlib.md5(content).hexdigest()[:8]

        # 时间戳
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # 保存文件
        new_filename = f"{name}_{timestamp}_{file_md5}{extension}"
        save_path = os.path.join("upload/files", new_filename)

        async with aiofiles.open(save_path,"wb") as f:
            await f.write(content)

        filenames.append({
            "original": original_name,
            "saved":new_filename,
            "md5":file_md5

        })
    return ApiResponse.success(data={"filenames":filenames})
     #     with open(save_path, "wb") as f:
     #         f.write(file.file.read())
     #     filenames.append(filename)
     # return ApiResponse.success(data={"filenames": filenames})
