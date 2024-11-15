from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.productSchema import Product, Review, ReviewBase
from schemas.userSchema import UserCreate, UserUpdate, User
from controllers import spiderController
from utils.utils import get_current_user
router = APIRouter()


@router.get("/api/spider/get-product", response_model=List[Product])
def get_product(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    return spiderController.get_product(db=db, page=page, page_size=page_size)
