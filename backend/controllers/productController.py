import json

from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from starlette.responses import JSONResponse

from models.model import Product, Review, User
from pydantic import BaseModel
from sqlalchemy.orm import Session
from schemas.productSchema import ReviewBase, ProductCreate
from utils.utils import get_current_user




def create_product(db: Session, product: ProductCreate):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category=product.category,
        image=product.image,
        countInStock=product.countInStock,
        url=product.url,
        platform=product.platform
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# 获取所有产品
def get_products(db: Session, page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    products = db.query(Product).offset(skip).limit(page_size).all()
    return products


# 获取单个产品
def get_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for review in product.reviews:
        user = db.query(User).filter(User.id == review.user_id).first()
        review.name = user.name
    return product


# 创建产品评论
# def create_product_review(db: Session, product_id: int, review: ReviewCreate, current_user: User = Depends(get_current_user)):
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#
#     new_review = Review(
#         rating=review.rating,
#         comment=review.comment,
#         user_id=current_user.id,
#         product_id=product_id
#     )
#     db.add(new_review)
#     product.numReviews += 1
#     product.rating = (product.rating * (product.numReviews - 1) + review.rating) / product.numReviews
#     db.commit()
#     db.refresh(new_review)
#     return new_review
def create_product_review(
        db: Session,
        product_id: int,
        review: ReviewBase,
        current_user: User = Depends(get_current_user)  # 从JWT获取当前用户
):
    if not isinstance(current_user, User):
        return JSONResponse(status_code=400, content={"detail": str(current_user)})
    try:
        # 查询产品是否存在
        product = db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        # 使用当前登录的用户创建新的评论
        new_review = Review(
            rating=review.rating,
            comment=review.comment,
            user_id=current_user.id,  # 使用从JWT获取的user_id
            product_id=product_id
        )

        db.add(new_review)

        # 更新产品的评分和评论数
        product.numReviews += 1
        product.rating = (product.rating * (product.numReviews - 1) + review.rating) / product.numReviews

        # 提交事务并刷新评论对象
        db.commit()
        db.refresh(new_review)

        return new_review
    except HTTPException as http_exc:
        # 捕获HTTPException并返回正确的响应
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})
    except Exception as e:
        # 其他类型的异常返回错误信息
        return JSONResponse(status_code=500, content={"error": str(e)})
# 获取相关产品
def get_related_product_by_id(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    related_products = db.query(Product).filter(Product.category == product.category, Product.id != product.id).all()
    return related_products


# 获取顶级评分产品
def get_top_products(db: Session):
    products = db.query(Product).order_by(Product.rating.desc()).limit(10).all()
    return products


def get_product_price_history(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.historyPrice