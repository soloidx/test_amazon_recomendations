from tar_api.models.products import Review
from typing import Optional
from sqlalchemy.orm import Session

from tar_api.schema import products as products_schema
from tar_api import models

ITEMS_BY_PAGE = 10


def get_product_by_asin(db: Session, asin: str):
    product = db.query(models.Product).filter_by(asin=asin).first()
    return product


def create_product(db: Session, product: products_schema.ProductBase):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def search_products(db: Session, *, search_string: Optional[str], page: int):
    products = db.query(models.Product)
    if search_string is not None:
        # we could also filter in other fields like asin
        products = products.filter(
            models.Product.name.ilike(f"%{search_string}%")
        )

    count = products.count() / ITEMS_BY_PAGE

    products = products.limit(ITEMS_BY_PAGE).offset((page - 1) * ITEMS_BY_PAGE)

    return {
        "data": products.all(),
        "total_pages": count,
        "current_page": page,
    }


def check_review_by_id(db: Session, review_id: str):
    review = db.query(models.Review).filter_by(review_id=review_id).count()
    return review > 0


def create_review(db: Session, review: products_schema.ReviewBase):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews_by_product(db: Session, product_id: int, page: int):
    reviews = db.query(models.Review).filter(
        models.Review.product_id == product_id
    )

    count = reviews.count() / ITEMS_BY_PAGE

    reviews = reviews.limit(ITEMS_BY_PAGE).offset((page - 1) * ITEMS_BY_PAGE)

    return {
        "data": reviews.all(),
        "total_pages": count,
        "current_page": page,
    }
