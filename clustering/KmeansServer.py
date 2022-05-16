import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from kMeans import Kmeans

app = FastAPI()
model: Kmeans = np.load('./5cluster.pkl', allow_pickle=True)


@app.get("/")
def classify_candidate(candidate):
    # convert candidate to mathcing representation
    # find which cluster the candidate belongs to
    # get innner cluster segemntation of companys

    return {"Hello": "World"}


@app.post("/")
def read_root():
    return {"Bye": "World"}
