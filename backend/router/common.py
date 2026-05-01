from fastapi import APIRouter, UploadFile, File
from werkzeug.utils import secure_filename
import os
import hashlib
from datetime import datetime
from common.constant import ImageType
from domain.vo import ImageVO, NoticeVO
from service import CacheKey
from common.utils import ApiResponse, CacheUtils
from common.settings import app_settings
from common.exception import BusinessException
import aiofiles
from common.database import Image, SessionFactory, Notice
import json
from common.utils import Logger
router = APIRouter(
    prefix='/common',
    tags=["公共接口"]
)

os.makedirs(app_settings.upload.UPLOAD_DIR, exist_ok=True)

@router.post(
    "/upload",
    summary="多文件上传",
    description="批量上传文件，自动生成唯一文件名"
)
async def upload(
    files: list[UploadFile] = File(..., description="多文件上传")
):
    if not files:
        raise BusinessException("未上传任何文件")

    result = []

    for file in files:
        try:
            original_name = secure_filename(file.filename or "file")

            if len(original_name) > 100:
                raise BusinessException("文件名过长（最长100字符）")

            # 取文件后缀
            _, ext = os.path.splitext(original_name)
            content = await file.read()

            if len(content) > app_settings.upload.MAX_FILE_SIZE * 1024 * 1024:
                raise BusinessException(f"文件大小超出限制（最大{app_settings.upload.MAX_FILE_SIZE}MB）")

            file_md5 = hashlib.md5(content).hexdigest()  # 32位
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # 14位
            
            # 最终固定长度文件名：时间戳 + MD5，长度完全一致
            save_name = f"{timestamp}_{file_md5}{ext}"

            # 保存路径
            save_path = os.path.join(app_settings.upload.UPLOAD_DIR, save_name)

            async with aiofiles.open(save_path, "wb") as f:
                await f.write(content)

            result.append({
                "name": original_name,
                "save_name": save_name,  # 所有文件这个长度完全一样
                "md5": file_md5[:8],
                "path": save_path
            })

        except Exception as e:
            result.append({
                "name": file.filename,
                "error": str(e)
            })

    return ApiResponse.page(
        list=result,
        total=len(result),
        page_num=1,
        page_size=len(result)
    )


@router.get("/banner")
async def get_banner():
    Logger.info("从缓存查询轮播图信息")
    cache = CacheUtils.get(CacheKey.banner())

    if cache:
        Logger.info("轮播图缓存命中，返回缓存")
        return ApiResponse.success(json.loads(cache))

    Logger.info("轮播缓存未命中，查询数据库")
    with SessionFactory() as db:
        # 查库 + 序列化
        queryset = db.query(Image).filter(
            Image.type == ImageType.Banner.value
        ).order_by(Image.index).all()
        
        data = [ImageVO.model_validate(b).model_dump() for b in queryset]

    # 写入缓存
    CacheUtils.set(CacheKey.banner(), json.dumps(data, ensure_ascii=False, default=str))
    Logger.info("轮播图信息已缓存")
    
    return ApiResponse.success(data)


@router.get("/notice")
async def get_notice():
    Logger.info("从缓存查询公告信息")
    cache_data = CacheUtils.get(CacheKey.notice())

    if cache_data:
        Logger.info("公告缓存命中，返回缓存")
        return ApiResponse.success(json.loads(cache_data))

    Logger.info("公告缓存未命中，查询数据库")
    with SessionFactory() as db:
        queryset = db.query(Notice).order_by(Notice.index).all()
        data = [NoticeVO.model_validate(n).model_dump() for n in queryset]

    CacheUtils.set(CacheKey.notice(), json.dumps(data, ensure_ascii=False, default=str))
    Logger.info("公告信息已缓存")

    return ApiResponse.success(data)
