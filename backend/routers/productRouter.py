from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.productSchema import Product, Review
from controllers import productController

router = APIRouter()


@router.get("/api/products", response_model=List[Product])
def get_products(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    return productController.get_products(db=db, page=page, page_size=page_size)

@router.get("/api/products/top", response_model=List[Product])
def get_top_products(db: Session = Depends(get_db)):
    return productController.get_top_products(db=db)

@router.get("/api/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return productController.get_product_by_id(db=db, product_id=product_id)


@router.post("/api/products/{product_id}/reviews", response_model=Review)
def create_product_review(product_id: int, review: Review, db: Session = Depends(get_db)):
    return productController.create_product_review(db=db, product_id=product_id, review=review)


@router.get("/api/products/{product_id}/related", response_model=List[Product])
def get_related_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return productController.get_related_product_by_id(db=db, product_id=product_id)



