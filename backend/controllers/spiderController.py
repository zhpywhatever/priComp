from datetime import datetime

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.model  import User
from schemas.userSchema import UserCreate, UserUpdate
from database import get_db
from utils.utils import authenticate_user, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from spider.main import get_lowest, spider_get_products
from controllers import productController
from models.model import Product
from schemas.productSchema import ProductCreate, PriceHistory
from utils.classify import classify

def get_product(db: Session,product_name:str):
    lowest_in_jd, lowest_in_tb = get_lowest(product_name)
    lowest = lowest_in_jd if lowest_in_jd[1] < lowest_in_tb[1] else lowest_in_tb
    new_product = ProductCreate(
        name=product_name,
        description=lowest[0],
        price=lowest[1],
        category=classify(lowest[0]),
        image=lowest[3],
        countInStock=0,
        historyPrice = [
        PriceHistory(price=lowest[1], timestamp=datetime.now().date().isoformat())
    ],
        url=lowest[2],
        platform='jd' if lowest[0] == lowest_in_jd[0] else 'tb',
        platform_id = lowest[4]
    )
    return productController.create_product(db=db, product=new_product)


def get_products(db: Session, product_name: str):
    try:
        jd_products, tb_products = spider_get_products(product_name)

        # 处理京东商品
        for product in jd_products:
            existing_product = db.query(Product).filter(
                Product.platform_id == product[4]).first()  # 查找是否已存在相同platform_id的商品

            # 如果商品存在，更新该商品
            if existing_product:
                existing_product.name = product_name
                existing_product.description = product[0]
                existing_product.price = product[1]
                existing_product.category = ""  # 你可以根据需要填充类别
                existing_product.image = product[3]
                existing_product.countInStock = 0  # 这里可以根据需要更新库存
                # existing_product.historyPrice.append(
                #     PriceHistory(price=product[1], timestamp=datetime.now().date().isoformat()))
                existing_product.update_history_price(product[1])
                existing_product.url = product[2]
                # 如果有需要，也可以更新其他字段
                db.commit()  # 提交更新
            else:
                # 如果商品不存在，创建新的商品
                new_product = ProductCreate(
                    name=product_name,
                    description=product[0],
                    price=product[1],
                    category="",
                    image=product[3],
                    countInStock=0,
                    historyPrice=[PriceHistory(price=product[1], timestamp=datetime.now().date().isoformat())],
                    url=product[2],
                    platform='jd',
                    platform_id=product[4]
                )
                productController.create_product(db=db, product=new_product)

        # 处理淘宝商品
        for product in tb_products:
            existing_product = db.query(Product).filter(
                Product.platform_id == product[4]).first()  # 查找是否已存在相同platform_id的商品

            # 如果商品存在，更新该商品
            if existing_product:
                existing_product.name = product_name
                existing_product.description = product[0]
                existing_product.price = product[1]
                existing_product.category = ""  # 你可以根据需要填充类别
                existing_product.image = product[3]
                existing_product.countInStock = 0  # 这里可以根据需要更新库存
                existing_product.historyPrice.append(
                    PriceHistory(price=product[1], timestamp=datetime.now().date().isoformat()))
                existing_product.url = product[2]
                # 如果有需要，也可以更新其他字段
                db.commit()  # 提交更新
            else:
                # 如果商品不存在，创建新的商品
                new_product = ProductCreate(
                    name=product_name,
                    description=product[0],
                    price=product[1],
                    category="",
                    image=product[3],
                    countInStock=0,
                    historyPrice=[PriceHistory(price=product[1], timestamp=datetime.now().date().isoformat())],
                    url=product[2],
                    platform='tb',
                    platform_id=product[4]
                )
                productController.create_product(db=db, product=new_product)

    except Exception as e:
        return e

    return jd_products, tb_products
