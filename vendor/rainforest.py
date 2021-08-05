import re
from datetime import datetime
from typing import Dict, List

import requests  # type: ignore

from settings import settings


class RainforesURLInvalidException(Exception):
    pass


class RainforesAPIException(Exception):
    pass


def get_asin_from_url(product_url) -> str:
    url_re = r"^https:\/\/[a-z\.]+\.amazon\.com\/.+\/dp\/(?P<asin>[A-Z 0-9]*)"

    match = re.match(url_re, product_url)

    if match is None:
        raise RainforesURLInvalidException(
            "Cannot extract the asin from:", product_url
        )

    return match.group("asin")


def get_product_by_url(url: str) -> Dict:
    """
    Given an Amazon URL get the product information
    """
    asin = get_asin_from_url(url)

    params = (
        f"api_key={settings.RAINFOREST_API_KEY}"
        f"&type=reviews"
        f"&amazon_domain=amazon.com"
        f"&asin={asin}"
        f"&review_stars=all_stars"
        f"&sort_by=most_recent"
    )
    response = requests.get(f"{settings.RAINFOREST_API_URL}/request?{params}")

    try:
        response.raise_for_status()
    except BaseException as e:
        raise RainforesAPIException(
            "There was an internal error with the API"
        ) from e

    data = response.json()

    return {
        "asin": data["product"]["asin"],
        "name": data["product"]["title"],
        "image_url": data["product"]["image"],
        "link": data["product"]["link"],
        "rating": data["summary"]["rating"],
    }


def get_reviews_by_asin(asin: str, page: int = 1) -> List[Dict]:
    """
    Given an Amazon URL get the product information
    """
    params = (
        f"api_key={settings.RAINFOREST_API_KEY}"
        f"&type=reviews"
        f"&amazon_domain=amazon.com"
        f"&asin={asin}"
        f"&review_stars=all_stars"
        f"&sort_by=most_recent"
        f"&page={page}"
    )
    response = requests.get(f"{settings.RAINFOREST_API_URL}/request?{params}")

    try:
        response.raise_for_status()
    except BaseException as e:
        raise RainforesAPIException(
            "There was an internal error with the API"
        ) from e

    data = response.json()
    raw_reviews = data["reviews"]
    reviews = [
        {
            "review_id": x["id"],
            "title": x["title"],
            "body": x["body"],
            "body_html": x["body_html"],
            "rating": x["rating"],
            "datetime": datetime.strptime(
                x["date"]["utc"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            "verified_purchase": x["verified_purchase"],
            "attributes": [] if "attributes" not in x else x["attributes"],
        }
        for x in raw_reviews
    ]

    return reviews
