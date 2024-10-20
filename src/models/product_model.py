from typing import List, Optional
from pydantic import BaseModel

class Product(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    stock: float
    category: str
    price: float
    date: str
    manufacturer: str
    email: str
    country: str