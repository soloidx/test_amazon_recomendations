from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from tar_api import crud
from tar_api.schema.api_v1 import AddRequest
from tar_api.schema import products as products_schema
from tar_api.deps import get_db
from tar_api import tasks

from vendor import rainforest


router = APIRouter(prefix="/v1", tags=["version 1"])


@router.post("/products/add/", response_model=products_schema.Product)
def add_product(request: AddRequest, db: Session = Depends(get_db)):
    """
    Adds a amazon url to the system
    """
    pre_product = crud.get_product_by_asin(
        db, rainforest.get_asin_from_url(request.url)
    )
    if pre_product is not None:
        tasks.process_reviews(pre_product.asin)
        return pre_product

    product_raw = rainforest.get_product_by_url(request.url)
    product_base = products_schema.ProductBase(**product_raw)

    product = crud.create_product(db, product_base)
    # TODO: make this in a queue
    tasks.process_reviews(product.asin)
    return product
