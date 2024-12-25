from datetime import datetime
from numbers import Number

from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel, Field, validator


# Pydantic model for Review
class ReviewBase(BaseModel):
    rating: float
    comment: Optional[str] = None


class Review(ReviewBase):
    id: int
    user_id: int
    product_id: int
    name: Optional[str] = None

    class Config:
        orm_mode = True


class PriceHistory(BaseModel):
    price: float
    timestamp: str

    def to_dict(self):
        # 返回一个字典，timestamp 会被格式化为 'YYYY-MM-DD'
        return {
            "price": self.price,
            "timestamp": self.timestamp  # 格式化时间到天
        }


# Pydantic model for Product
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    image: Optional[str] = None  # 设置为可选字段，默认值为 None
    countInStock: int
    historyPrice: Optional[List[PriceHistory]] = None
    url: str
    platform: str
    platform_id: Optional[int] = None

    def __post_init__(self):
        # 自动生成当前价格的历史记录
        if self.historyPrice is None:
            self.historyPrice = [
                PriceHistory(price=self.price, timestamp=datetime.now().isoformat())
            ]

class Product(ProductBase):
    id: int
    rating: Optional[float] = None
    numReviews: Optional[int] = None
    image: Optional[str] = None
    reviews: List[Review] = []  # 添加 reviews 数组
    countInStock: Optional[int] = None
    historyPrice: Optional[List[PriceHistory]] = None
    url: Optional[str] = None
    platform: Optional[str] = None
    platform_id: Optional[int] = None

    class Config:
        orm_mode = True
