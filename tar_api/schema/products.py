from datetime import datetime
from typing import List, Dict, Optional

from pydantic import BaseModel


class ReviewBase(BaseModel):
    title: str
    body: str
    body_html: str
    product_id: int
    rating: float
    datetime: datetime
    verified_purchase: bool
    attributes: List[Dict]


class ReviewCreate(ReviewBase):
    review_id: str
    keywords: str


class Review(ReviewBase):
    id: str

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    asin: str
    name: str
    image_url: str
    link: str
    rating: float


class Product(ProductBase):
    id: int
    top_keywords: Optional[List] = []
    # reviews: List[Review]

    class Config:
        orm_mode = True
