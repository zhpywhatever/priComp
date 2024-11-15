from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.model  import User
from schemas.userSchema import UserCreate, UserUpdate
from database import get_db
from utils.utils import authenticate_user, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from spider.main import compare_prices


# 注册新用户
def get_product(user: UserCreate, db: Session):
    return

# 关注用户
def follow_user(target_user_id: int, db: Session, current_user: User = Depends(get_current_user)):
    try:
        target_user = db.query(User).filter(User.id == target_user_id).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="目标用户不存在")
        if target_user.id == current_user.id:
            raise HTTPException(status_code=403, detail="不能关注自己")
        if current_user.id not in target_user.followers:
            target_user.followers.append(current_user.id)
            current_user.followings.append(target_user.id)
            db.commit()
        return {"message": "关注成功"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}

# 取消关注
def unfollow_user(target_user_id: int, db: Session, current_user: User = Depends(get_current_user)):
    try:
        target_user = db.query(User).filter(User.id == target_user_id).first()
        if not target_user:
            raise HTTPException(status_code=404, detail="目标用户不存在")
        if current_user.id in target_user.followers:
            target_user.followers.remove(current_user.id)
            current_user.followings.remove(target_user.id)
            db.commit()
        return {"message": "取消关注成功"}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}
