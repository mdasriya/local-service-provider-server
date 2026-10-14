from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.core.dependencies import get_current_user

from app.modules.chat.schema import (
    CreateConversationSchema,
    SendMessageSchema
)

from app.modules.chat.controller import (
    create_conversation_controller,
    send_message_controller,
    get_messages_controller,
get_my_conversations_controller
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


# ======================================
# CREATE CONVERSATION
# ======================================

@router.post("/conversation")
def create_conversation(

    conversation: CreateConversationSchema,

    current_user = Depends(get_current_user),

    db: Session = Depends(get_db)
):

    return create_conversation_controller(
        conversation,
        current_user,
        db
    )


# ======================================
# SEND MESSAGE
# ======================================

@router.post("/message")
def send_message(

    message: SendMessageSchema,

    current_user = Depends(get_current_user),

    db: Session = Depends(get_db)
):

    return send_message_controller(
        message,
        current_user,
        db
    )


# ======================================
# GET MESSAGES
# ======================================

@router.get("/messages/{conversation_id}")
def get_messages(

    conversation_id: int,

    current_user = Depends(get_current_user),

    db: Session = Depends(get_db)
):

    return get_messages_controller(
        conversation_id,
        current_user,
        db
    )

# ======================================
# GET MY CONVERSATIONS
# ======================================

@router.get("/conversations")
def get_my_conversations(

    current_user = Depends(get_current_user),

    db: Session = Depends(get_db)
):

    return get_my_conversations_controller(
        current_user,
        db
    )