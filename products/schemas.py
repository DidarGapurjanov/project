from pydantic import BaseModel


class Product1(BaseModel):
    name: str
    price: float
    description: str
