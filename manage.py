#!/usr/bin/env python

# import subprocess

import typer
import uvicorn  # type: ignore

manager = typer.Typer()


@manager.command()
def runserver(reload: bool = True):
    uvicorn.run(
        "tar_api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=reload,
    )


@manager.command()
def runworker(reload: bool = True):
    pass


if __name__ == "__main__":
    manager()
