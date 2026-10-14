from pydantic import BaseModel


class NotificationResponseSchema(BaseModel):

    id: int

    title: str

    message: str

    is_read: bool

    class Config:

        from_attributes = True