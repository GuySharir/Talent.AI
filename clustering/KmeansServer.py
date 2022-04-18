from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()


def test():
    time.sleep(10)


@app.get("/")
def read_root():
    test()
    return {"Hello": "World"}


@app.post("/")
async def read_root():
    return {"Bye": "World"}
