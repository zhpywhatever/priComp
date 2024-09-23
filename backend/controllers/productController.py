from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.model import Product, Review
from pydantic import BaseModel
from sqlalchemy.orm import Session


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
def create_product_review(db: Session, product_id: int, review: ReviewCreate):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    new_review = Review(
        name=review.name,
        rating=review.rating,
        comment=review.comment,
        user_id=review.user_id,
        role=review.role,
        image=review.image,
        product_id=product_id
    )
    db.add(new_review)
    product.num_reviews += 1
    product.rating = (product.rating * (product.num_reviews - 1) + review.rating) / product.num_reviews
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
