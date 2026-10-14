from pydantic import BaseModel


class FavoriteCreateSchema(BaseModel):

    service_id: int