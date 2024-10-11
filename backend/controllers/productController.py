from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from models.model import Product, Review, User
from pydantic import BaseModel
from sqlalchemy.orm import Session

from utils.utils import get_current_user


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str


class ReviewCreate(BaseModel):
    name: str
    rating: int
    comment: str
    user_id: int
    role: str
    image: str = None


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
        review: ReviewCreate,
        current_user: User = Depends(get_current_user)  # 从JWT获取当前用户
):
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
