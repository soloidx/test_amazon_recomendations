from sqlalchemy.orm import Session

from tar_api.schema import products as products_schema
from tar_api import models


def get_product_by_asin(db: Session, asin: str):
    product = db.query(models.Product).filter_by(asin=asin).first()
    return product


def create_product(db: Session, product: products_schema.ProductBase):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def check_review_by_id(db: Session, review_id: str):
    review = db.query(models.Review).filter_by(review_id=review_id).count()
    return review > 0


def create_review(db: Session, review: products_schema.ReviewBase):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
