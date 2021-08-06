from string import punctuation
from typing import Dict, Set

import spacy
from sqlalchemy.orm import Session
from rq.decorators import job  # type: ignore
from vendor import rainforest, redis

from tar_api import crud, deps
from tar_api.schema import products as products_schema


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Nlp(metaclass=SingletonMeta):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")


def get_keywords(nlp, text: str) -> Set:
    pos_tag = ["PROPN", "ADJ", "NOUN"]
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if (
            token.text in nlp.Defaults.stop_words
            or token.text in punctuation
            or len(token.text) < 3
        ):
            continue
        if token.pos_ in pos_tag:
            result.append(token.text)

    return set(result)


def save_review(nlp, db: Session, review: Dict, product_id: int, asin: str):

    if crud.check_review_by_id(db, review["review_id"]):
        return

    keys = get_keywords(nlp, review["body"])
    review["keywords"] = ",".join(keys)
    crud.create_review(
        db,
        products_schema.ReviewCreate(**review, product_id=product_id),
    )
    redis.increase_keys_for_product(asin, keys)


@job("high", connection=redis.get_connection())
def process_reviews(asin: str, page: int = 1):
    nlp = Nlp().nlp
    product = None
    with deps.get_db_context() as db:
        product = crud.get_product_by_asin(db, asin)

    if product is None:
        return

    data = rainforest.get_reviews_by_asin(asin, page)
    reviews = data["reviews"]

    with deps.get_db_context() as db:
        for review in reviews:
            save_review(nlp, db, review, product.id, asin)

    # call to a new job if there are still more data to process
    total_pages = data["total_pages"]
    if page < total_pages:
        process_reviews.delay(asin, page + 1)
