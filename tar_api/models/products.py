from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    Numeric,
    DateTime,
    Boolean,
    JSON,
)
from sqlalchemy.orm import relationship


from tar_api.models.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    asin = Column(String, unique=True, index=True)
    name = Column(String)
    image_url = Column(String)
    link = Column(String)
    rating = Column(Numeric)

    reviews = relationship("Review", back_populates="product")  # type: ignore


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(String, unique=True, index=True)
    title = Column(String)
    body = Column(Text)
    body_html = Column(Text)
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Numeric)
    datetime = Column(DateTime)
    verified_purchase = Column(Boolean)
    attributes = Column(JSON)
    keywords = Column(String, default="")

    product = relationship("Product", back_populates="reviews")  # type: ignore
