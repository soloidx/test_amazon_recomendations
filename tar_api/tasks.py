from vendor import rainforest
from tar_api import crud, deps
from tar_api.schema import products as products_schema


def process_reviews(asin: str, page: int = 1):
    product = None
    with deps.get_db_context() as db:
        product = crud.get_product_by_asin(db, asin)

    if product is None:
        return

    reviews = rainforest.get_reviews_by_asin(asin)

    with deps.get_db_context() as db:
        for review in reviews:
            print(review)
            crud.create_review(
                db, products_schema.ReviewBase(**review, product_id=product.id)
            )
    # TODO: per each review get the keywords
    # TODO: increase the counter in redis of keywords
