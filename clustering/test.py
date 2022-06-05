from datetime import datetime
from program.DistanceFlow import freq_rep_dist
from kMeans import Kmeans
import numpy as np
import pandas as pd
import pickle as pkl


def create_matrix():
    with open('../five_my.pkl', 'rb') as inp:
        model: Kmeans = pkl.load(inp)

    data = model.data
    order = model.order

    size = len(data)
    print(model.data)

    distances = np.zeros((10, 10))
    start = 0

    for i in range(size):
        if i == 10:
            break
        if i == 0:
            start = datetime.now()
        if i == 1:
            now = datetime.now()
            diff = now - start
            print(f"total time to calculate will be: {diff.total_seconds() / 60 * size} minutes")

        print(f"now calculating the {i} row out of {size}")

        first = list(data.iloc[i])
        # print(first)

        for j in range(i, 10):
            second = list(data.iloc[j])
            distances[i][j] = distances[j][i] = freq_rep_dist(first, second)

    with open('matrix.pkl', 'wb') as f:
        pkl.dump(distances, f)

    print(distances)


create_matrix()

# with open('./matrix.pkl', 'rb') as inp:
#     x = pkl.load(inp)
#     print(x)
