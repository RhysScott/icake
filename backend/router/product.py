from tkinter import image_names

from fastapi import APIRouter
from router.common import ImageType
from common.database import Image, SessionFactory
from service import CacheKey, CacheUtils
from domain.vo import ProductVO
from common.database import Product

from common.utils import ApiResponse, Logger


router = APIRouter(prefix='/product', tags=["商品接口"])

@router.get("/")
async def get_product(id: int):
    Logger.info("从缓存获取商品信息")
    cache_key = CacheKey.product(id)
    cache = CacheUtils.get(cache_key)

    # 缓存有数据 → 直接返回
    if cache is not None:
        Logger.info("商品信息缓存命中，返回缓存")
        return ApiResponse.success(cache)

    Logger.info("商品缓存未命中，查询数据库")
    with SessionFactory() as db:
        product = db.query(Product).filter(Product.id == id, Product.status == 1).first()

        # 商品不存在 → 缓存空值
        if not product:
            CacheUtils.set(cache_key, None)
            Logger.info("商品不存在，已缓存空值")
            return ApiResponse.fail("商品不存在")

        # 查询关联图片
        images = db.query(Image).filter(Image.rel_id == product.id)
        cover_url = images.filter(Image.type == ImageType.ProductCover.value).first()
        banner_urls = images.filter(Image.type == ImageType.ProductBanner.value).order_by(Image.index).all()
        detail_urls = images.filter(Image.type == ImageType.ProductDetail.value).order_by(Image.index).all()

        # 组装返回数据
        data = ProductVO.model_validate(product).model_dump()
        data.update({
            "cover_url": cover_url.path if cover_url else None,
            "banner_urls": [b.path for b in banner_urls] if banner_urls else [],
            "detail_urls": [d.path for d in detail_urls] if detail_urls else []
        })

    # 写入缓存
    CacheUtils.set(cache_key, data)
    Logger.info("商品信息已缓存")

    return ApiResponse.success(data)


