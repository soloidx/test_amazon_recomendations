from string import punctuation
from typing import Set, Dict
import spacy
from sqlalchemy.orm import Session
from vendor import rainforest
from tar_api import crud, deps
from tar_api.schema import products as products_schema


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


def save_review(nlp, db: Session, review: Dict, product_id: int):

    if crud.check_review_by_id(db, review["review_id"]):
        return

    keys = get_keywords(nlp, review["body"])
    review["keywords"] = ",".join(keys)
    crud.create_review(
        db,
        products_schema.ReviewCreate(**review, product_id=product_id),
    )


def process_reviews(asin: str, page: int = 1):
    nlp = spacy.load("en_core_web_sm")
    product = None
    with deps.get_db_context() as db:
        product = crud.get_product_by_asin(db, asin)

    if product is None:
        return

    reviews = rainforest.get_reviews_by_asin(asin)

    with deps.get_db_context() as db:
        for review in reviews:
            save_review(nlp, db, review, product.id)
    # TODO: per each review get the keywords
    # TODO: increase the counter in redis of keywords
