import uvicorn
import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle as pkl

sys.path.insert(0, os.path.abspath(os.path.abspath(os.getcwd())))
print(os.getcwd())
from clustering.kMeans import Kmeans

app = FastAPI()
from pydantic import BaseModel


class Candidate(BaseModel):
    values: list


with open('./3cluster.pkl', 'rb') as file:
    model = pkl.load(file)


@app.post("/")
def classify_candidate(candidate: Candidate):
    cluster = model.predict(candidate)
    companys = model.percents[cluster]

    return companys


# @app.post("/")
# def read_root():
#     return {"Bye": "World"}


if __name__ == "__main__":
    uvicorn.run("KmeansServer:app", host="127.0.0.1", port=3000)
