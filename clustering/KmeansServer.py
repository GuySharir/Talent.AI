from typing import List
from pydantic import BaseModel
from clustering.kMeans import Kmeans
import uvicorn
import sys
import os
from fastapi import FastAPI
import pickle as pkl

sys.path.insert(0, os.path.abspath(os.path.abspath(os.getcwd())))

app = FastAPI()


class Candidate(BaseModel):
    _id: str = None
    full_name: str = None
    first_name: str = None
    last_name: str = None
    gender: str = None
    birth_year: int = None
    birth_date: str = None
    industry: str = None
    job_title: str = None
    job_title_role: str = None
    job_title_sub_role: str = None
    job_title_levels: list = None
    job_company_id: str = None
    job_company_name: str = None
    job_start_date: str = None
    interests: list = None
    skills: list = None
    experience: list = None
    education: list = None
    googleID: str = None
    email: str = None


class Bias(BaseModel):
    age: bool = False
    gender: bool = False


with open('./clustering/demo2.pkl', 'rb') as file:
    model: Kmeans = pkl.load(file)


def remove_id(candidate: Candidate):
    candidate.__delattr__("googleID")
    candidate.__delattr__("email")

    for item in candidate.education:
        if "_id" in item:
            del item["_id"]

    for item in candidate.experience:
        if "_id" in item:
            del item["_id"]


@app.post("/api/candidate")
def classify_candidate(candidate: Candidate):
    remove_id(candidate)
    return model.predict(vars(candidate))


@app.post("/api/company")
def calc_candidates_order(candidates: List[Candidate], job_offer: Candidate, bias: Bias):
    remove_id(job_offer)
    for candidate in candidates:
        remove_id(candidate)

    order = model.company_order(candidates, vars(
        job_offer), gender=bias.gender, age=bias.age)
    return order


if __name__ == "__main__":
    uvicorn.run("KmeansServer:app", host="127.0.0.1", port=4000)
