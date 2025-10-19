from pydantic import BaseModel


class RectRequest(BaseModel):
    x: int
    y: int
    width: int
    height: int
