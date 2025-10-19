from pydantic import BaseModel


class ScreenInfoOut(BaseModel):
    x: int
    y: int
    width: int
    height: int
    name: str
    is_primary: bool
    width_mm: int
    height_mm: int