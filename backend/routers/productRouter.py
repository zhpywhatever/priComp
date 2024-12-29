from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas.productSchema import Product, Review, ReviewBase
from schemas.userSchema import UserCreate, UserUpdate, User
from controllers import productController
from utils.utils import get_current_user
router = APIRouter()


@router.get("/api/products")
def get_products(
        keyword: Optional[str] = Query(None),  # 默认值为 None
        priceRange: Optional[List[int]] = Query([0, 1000]),  # 默认值为 [0, 1000]，可以传入其他范围
        rating: Optional[int] = Query(None),  # 默认值为 None
        platform: Optional[str] = Query(None),  # 默认值为 None
        inStock: Optional[bool] = Query(None),  # 默认值为 None
        page: int = Query(1, ge=1),  # page 参数，不需要改变
        page_size: int = Query(10, ge=1),  # page_size 参数，不需要改变
        db: Session = Depends(get_db)  # 获取数据库会话
):
    filters = {
        "keyword": keyword,
        "priceRange": priceRange,
        "rating": rating,
        "platform": platform,
        "inStock": inStock,
    }
    return productController.get_filtered_products(db=db, filters=filters, page=page, page_size=page_size)


@router.get("/api/products/top", response_model=List[Product])
def get_top_products(db: Session = Depends(get_db)):
    return productController.get_top_products(db=db)

@router.get("/api/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return productController.get_product_by_id(db=db, product_id=product_id)


@router.post("/api/products/{product_id}/reviews", response_model=Review)
def create_product_review(product_id: int, review: ReviewBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return productController.create_product_review(db=db, product_id=product_id, review=review, current_user=current_user)

@router.get("/api/products/{product_id}/price-history")
def get_product_price_history(product_id: int,  db: Session = Depends(get_db)):
    return productController.get_product_price_history(db=db, product_id=product_id)


@router.get("/api/products/{product_id}/related", response_model=List[Product])
def get_related_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return productController.get_related_product_by_id(db=db, product_id=product_id)


