from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.model  import User
from schemas.userSchema import UserCreate, UserUpdate
from database import get_db
from utils.utils import authenticate_user, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from spider.main import get_lowest
from controllers import productController
from models.model import Product
from schemas.productSchema import ProductCreate


def get_product(db: Session,product_name:str):
    lowest_in_jd, lowest_in_tb = get_lowest(product_name)
    lowest = lowest_in_jd if lowest_in_jd[1] < lowest_in_tb[1] else lowest_in_tb
    new_product = ProductCreate(
        name=product_name,
        description=lowest[0],
        price=lowest[1],
        category="",
        image=lowest[3],
        countInStock=0,
        url=lowest[2],
        platform='jd' if lowest[0] == lowest_in_jd[0] else 'tb'

    )
    return productController.create_product(db=db, product=new_product)
