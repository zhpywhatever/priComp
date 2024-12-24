from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.productSchema import Product, Review, ReviewBase
from schemas.userSchema import UserCreate, UserUpdate, User
from controllers import spiderController
from utils.utils import get_current_user
router = APIRouter()


@router.get("/api/spider/get-product/{product_name}")
def get_product( product_name: str, db: Session = Depends(get_db)):
    return spiderController.get_product(db=db,product_name = product_name)
