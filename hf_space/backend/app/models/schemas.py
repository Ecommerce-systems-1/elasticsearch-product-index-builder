from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    description: str
    category: str
    color: str
    price: float
    tags: list[str]
    brand: str
    in_stock: bool
    created_at: str


class SearchHit(BaseModel):
    product_id: str
    name: str
    category: str
    color: str
    price: float
    brand: str
    score: float
    matched_fields: list[str]
    highlight: str
