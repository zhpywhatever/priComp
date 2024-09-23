from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import os
import bcrypt
import secrets
from datetime import datetime, timedelta
from models import Base

# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    image = Column(String(255), default='/images/airpods.jpg')
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    location = Column(String(100), default='火星')
    gender = Column(String(10), default='保密')
    biography = Column(String(255), default='我的个性签名')
    role = Column(String(20), default='user')
    followers = Column(JSON, default=[])
    followings = Column(JSON, default=[])
    reset_password_token = Column(String(255), nullable=True)
    reset_password_expire = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with Review
    reviews = relationship("Review", back_populates="user")

    def __init__(self, name, email, password, image, location='火星', gender='保密', biography='我的个性签名', role='user'):
        self.name = name
        self.email = email
        self.set_password(password)
        self.image = image
        self.location = location
        self.gender = gender
        self.biography = biography
        self.role = role

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def get_reset_password_token(self):
        reset_token = secrets.token_hex(20)
        self.reset_password_token = bcrypt.hashpw(reset_token.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.reset_password_expire = datetime.utcnow() + timedelta(minutes=10)
        return reset_token

# Product Model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=True)
    numReviews = Column(Integer, default=0)
    image = Column(String(255), nullable=True)
    category = Column(String(100), nullable=False)

    # Relationship with Review
    reviews = relationship("Review", back_populates="product")

# Review Model
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float, nullable=False)
    comment = Column(Text, nullable=True)

    # Foreign keys
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

    # Relationships
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
