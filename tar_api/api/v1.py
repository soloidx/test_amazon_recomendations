from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from tar_api import crud
from tar_api.schema.api_v1 import AddRequest, PaginatedResponse
from tar_api.schema import products as products_schema
from tar_api.deps import get_db
from tar_api import tasks

from vendor import rainforest, redis


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
        tasks.process_reviews.delay(pre_product.asin)
        return pre_product

    product_raw = rainforest.get_product_by_url(request.url)
    product_base = products_schema.ProductBase(**product_raw)

    product = crud.create_product(db, product_base)
    tasks.process_reviews.delay(product.asin)
    return product


@router.get(
    "/products/",
    response_model=PaginatedResponse[List[products_schema.Product]],
)
def get_products(
    q: Optional[str] = None, page: int = 1, db: Session = Depends(get_db)
):
    """
    Get a list of products

    Params:

    - q: A string for search in the product title
    - page: A number of the current page
    """
    results = crud.search_products(db, search_string=q, page=page)

    raw_data = results["data"]
    data = []
    total_pages = results["total_pages"]
    current_page = results["current_page"]

    for raw_prod in raw_data:
        product = products_schema.Product.from_orm(
            raw_prod
        )  # type: products_schema.Product
        product.top_keywords = redis.get_top_keys_from_product(product.asin)
        data.append(product)

    return PaginatedResponse[List[products_schema.Product]](
        total_pages=total_pages, current_page=current_page, data=data
    )


@router.get(
    "/products/{product_id}/reviews",
    response_model=PaginatedResponse[List[products_schema.Review]],
)
def get_reviews_by_product(
    product_id: int, page: int = 1, db: Session = Depends(get_db)
):
    """
    Get a list of reviews for a given product

    Path params:

    - product_id: the internal id (from the list of products) of the product

    Query params:

    - page: A number of the current page
    """
    results = crud.get_reviews_by_product(db, product_id=product_id, page=page)
    return PaginatedResponse(**results)
