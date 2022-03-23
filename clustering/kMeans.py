import json
import time

import numpy as np
import pandas as pd
import copy
from numpy.linalg import norm
# from program.DistanceFlow import DistanceFlow_
from distance.DistEnum import ListDistMethod
from distance.DistEnum import NestedDistMethod
from programFlow.DistFunctions import prepare_data_for_dist_calc_between_freq_vectors
from sklearn.utils import shuffle


def my_print(message):
    # print(inspect.stack()[1][3])
    print(message)


class Kmeans:

    def __init__(self, dataPath: str, n_clusters: int, max_iter: int = 20, random_state: int = None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.data: pd.DataFrame = None
        self.order: pd.DataFrame = None
        self.load_data(dataPath)
        self.centroids = []
        self.clusters = [[] for _ in range(n_clusters)]
        self.clusters_by_index = [[] for _ in range(n_clusters)]
        self.distance_calc = prepare_data_for_dist_calc_between_freq_vectors

        # print(self.data)

    def load_data(self, dataPath: str) -> pd.DataFrame:
        raw_data = np.load(dataPath, allow_pickle=True)
        data = []
        order = []
        for row in raw_data:
            data.append(list(row.values())[0])
            order.append(list(row.keys())[0])

        data = pd.DataFrame(data)
        order = pd.DataFrame(order)
        order.rename(columns={0: "name"}, inplace=True)

        combined: pd.DataFrame = pd.concat([data, order], axis=1)
        combined = shuffle(combined)

        combined = combined.sample(n=60)

        self.order = combined[['name']].copy()
        self.data = combined.copy().drop(['name'], axis=1)

    def initialize_centroids(self):
        size = self.data.shape[1]
        for i in range(self.n_clusters):
            # print(self.data.sample(n=1).values[0])
            self.centroids.append(self.data.sample(n=1).values[0])

    def clear_clusters(self):
        for i in range(self.n_clusters):
            self.clusters[i].clear()
            self.clusters_by_index[i].clear()

    def calc_centroids(self):
        i = 0
        for cluster in self.clusters:
            if len(cluster) != 0:
                tmp = np.average(cluster, axis=0)
                self.centroids[i] = tmp
            i += 1

    def find_closest_cluster(self, entry):
        distances = []
        for centroid in self.centroids:
            distances.append(self.distance_calc(entry, centroid))

        return np.argmin(distances)

    def add_to_cluster(self, cluster_idx, entry):
        self.clusters[cluster_idx].append(entry)

    def print_list(self, data):
        for row in data:
            print(row)

    def cluster_percents(self):

        percents = {}

        idx = 0
        for cluster in self.clusters_by_index:
            tmp = []
            for i in cluster:
                tmp.append(self.order.iloc[i]['name'])
            percents[idx] = tmp

    def fit(self):
        self.initialize_centroids()
        size = len(self.data)

        for iteration in range(self.max_iter):
            print(f"starting iteration {iteration}")
            self.clear_clusters()

            for idx in range(size):
                entry = list(self.data.iloc[idx])

                cluster_idx = self.find_closest_cluster(entry)
                self.add_to_cluster(cluster_idx, entry)
                self.clusters_by_index[cluster_idx].append(idx)

            old_centroids = copy.deepcopy(self.centroids)
            self.calc_centroids()

            stop = True
            for i in range(self.n_clusters):
                if np.all(old_centroids[i] != self.centroids[i]):
                    stop = False

            if stop:
                break

    def predict(self, entry):
        return self.centroids[self.find_closest_cluster(entry)]


if __name__ == "__main__":
    x = Kmeans('./tmp/fiveVecRep.npy', 6, 10)
    x.fit()

    for c in x.clusters_by_index:
        print(c)

    # d = []
    #
    # for i in range(5):
    #     d.append([1, 2, 3, 4, 5, 6, 7, 8])
    #
    # print(np.average(d, axis=0))

# for model in x.models:
#     my_print(model)
