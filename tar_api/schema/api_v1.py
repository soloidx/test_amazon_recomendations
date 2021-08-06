from typing import Any, TypeVar, Generic

from pydantic import BaseModel, HttpUrl
from pydantic.generics import GenericModel


class AddRequest(BaseModel):
    url: HttpUrl

    class Config:
        schema_extra = {
            "example": {
                "url": (
                    "https://www.amazon.com/"
                    "Nespresso-Espresso-Machine-DeLonghi-INCLUDED"
                    "/dp/B07YXMB9F9"
                )
            }
        }


DataT = TypeVar("DataT")


class PaginatedResponse(GenericModel, Generic[DataT]):
    data: DataT
    current_page: int
    total_pages: int
