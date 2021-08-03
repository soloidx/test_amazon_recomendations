from fastapi import FastAPI

from settings import settings
from tar_api.api import v1


app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(v1.router)


@app.get("/")
def read_root():
    return {"status": "ok"}
