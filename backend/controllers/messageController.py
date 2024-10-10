from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.model import Message

# 新建消息
async def add_message(message_data: dict, db: Session):
    new_message = Message(**message_data)
    try:
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 获取会话中的所有消息
async def get_messages(conversation_id: str, db: Session):
    try:
        messages = db.query(Message).filter_by(conversation_id=conversation_id).all()
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
