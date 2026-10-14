from app.modules.chat.service import (
    create_conversation_service,
    send_message_service,
    get_messages_service,
get_my_conversations_service
)


# ======================================
# CREATE CONVERSATION CONTROLLER
# ======================================

def create_conversation_controller(
    conversation_data,
    current_user,
    db
):

    return create_conversation_service(
        conversation_data,
        current_user,
        db
    )


# ======================================
# SEND MESSAGE CONTROLLER
# ======================================

def send_message_controller(
    message_data,
    current_user,
    db
):

    return send_message_service(
        message_data,
        current_user,
        db
    )


# ======================================
# GET MESSAGES CONTROLLER
# ======================================

def get_messages_controller(
    conversation_id,
    current_user,
    db
):

    return get_messages_service(
        conversation_id,
        current_user,
        db
    )

# ======================================
# GET MY CONVERSATIONS CONTROLLER
# ======================================

def get_my_conversations_controller(
    current_user,
    db
):

    return get_my_conversations_service(
        current_user,
        db
    )