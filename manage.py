#!/usr/bin/env python

# import subprocess

import typer
import uvicorn  # type: ignore

manager = typer.Typer()


@manager.command()
def runserver(reload: bool = True):
    uvicorn.run(
        "tar_api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=reload,
    )


if __name__ == "__main__":
    manager()
