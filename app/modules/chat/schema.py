from pydantic import BaseModel


class CreateConversationSchema(BaseModel):

    booking_id: int


class SendMessageSchema(BaseModel):

    conversation_id: int

    message: str