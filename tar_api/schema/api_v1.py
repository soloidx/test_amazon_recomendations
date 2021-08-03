from pydantic import BaseModel, HttpUrl


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
