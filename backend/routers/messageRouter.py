from fastapi import APIRouter, Depends
from controllers.messageController import add_message, get_messages
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

# 添加消息
@router.post("/")
async def create_message(message_data: dict, db: Session = Depends(get_db)):
    return await add_message(message_data, db)

# 获取会话中的所有消息
@router.get("/{conversation_id}")
async def fetch_messages(conversation_id: str, db: Session = Depends(get_db)):
    return await get_messages(conversation_id, db)
