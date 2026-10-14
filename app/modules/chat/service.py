from app.modules.chat.conversation_model import Conversation
from app.modules.chat.message_model import Message

from app.modules.bookings.model import Booking
from app.modules.providers.model import Provider
from sqlalchemy import or_


# ======================================
# CREATE CONVERSATION
# ======================================

def create_conversation_service(
    conversation_data,
    current_user,
    db
):

    booking = db.query(Booking).filter(
        Booking.id == conversation_data.booking_id
    ).first()

    if not booking:

        return {
            "success": False,
            "message": "Booking not found"
        }

    # Only booking customer can create conversation
    if booking.customer_id != current_user.id:

        return {
            "success": False,
            "message": "Unauthorized conversation access"
        }

    existing_conversation = db.query(Conversation).filter(
        Conversation.booking_id == booking.id
    ).first()

    if existing_conversation:

        return {
            "success": True,
            "message": "Conversation already exists",
            "data": existing_conversation
        }

    conversation = Conversation(
        booking_id=booking.id,
        customer_id=booking.customer_id,
        provider_id=booking.provider_id
    )

    db.add(conversation)

    db.commit()

    db.refresh(conversation)

    return {
        "success": True,
        "message": "Conversation created successfully",
        "data": conversation
    }


# ======================================
# SEND MESSAGE
# ======================================

def send_message_service(
    message_data,
    current_user,
    db
):

    conversation = db.query(Conversation).filter(
        Conversation.id == message_data.conversation_id
    ).first()

    if not conversation:

        return {
            "success": False,
            "message": "Conversation not found"
        }

    provider = db.query(Provider).filter(
        Provider.id == conversation.provider_id
    ).first()

    provider_user_id = provider.user_id if provider else None

    allowed_users = [
        conversation.customer_id,
        provider_user_id
    ]

    if current_user.id not in allowed_users:

        return {
            "success": False,
            "message": "Unauthorized message access"
        }

    new_message = Message(
        conversation_id=conversation.id,
        sender_id=current_user.id,
        message=message_data.message
    )

    db.add(new_message)

    db.commit()

    db.refresh(new_message)

    return {
        "success": True,
        "message": "Message sent successfully",
        "data": new_message
    }


# ======================================
# GET CONVERSATION MESSAGES
# ======================================

def get_messages_service(
    conversation_id,
    current_user,
    db
):

    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()

    if not conversation:

        return {
            "success": False,
            "message": "Conversation not found"
        }

    provider = db.query(Provider).filter(
        Provider.id == conversation.provider_id
    ).first()

    provider_user_id = provider.user_id if provider else None

    allowed_users = [
        conversation.customer_id,
        provider_user_id
    ]

    if current_user.id not in allowed_users:

        return {
            "success": False,
            "message": "Unauthorized conversation access"
        }

    messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(
        Message.created_at.asc()
    ).all()

    return {
        "success": True,
        "message": "Messages fetched successfully",
        "data": messages
    }

# ======================================
# GET MY CONVERSATIONS
# ======================================

def get_my_conversations_service(
    current_user,
    db
):

    provider = db.query(Provider).filter(
        Provider.user_id == current_user.id
    ).first()

    provider_id = provider.id if provider else None

    conversations = db.query(Conversation).filter(

        or_(

            Conversation.customer_id == current_user.id,

            Conversation.provider_id == provider_id
        )

    ).order_by(
        Conversation.created_at.desc()
    ).all()

    return {
        "success": True,
        "message": "Conversations fetched successfully",
        "data": conversations
    }