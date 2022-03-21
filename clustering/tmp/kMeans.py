import json

import numpy as np
import pandas as pd
from program.DistanceFlow import DistanceFlow
from distance.DistEnum import ListDistMethod
from distance.DistEnum import NestedDistMethod


def my_print(message):
    # print(inspect.stack()[1][3])
    print(message)


class Kmeans:

    def __init__(self, dataPath: str, n_clusters: int, max_iter: int = 20, random_state: int = None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.data: pd.DataFrame = None
        self.load_data(dataPath)
        self.centroids = []
        self.clusters = [[] for _ in range(n_clusters)]
        self.distance_calc: DistanceFlow = DistanceFlow(False, False, ListDistMethod.intersection,
                                                        NestedDistMethod.all_items)
        self.dp = {}

    def load_data(self, dataPath: str) -> pd.DataFrame:
        with open(dataPath, 'r') as file:
            json_data = json.load(file)
            self.data = pd.DataFrame.from_records(json_data)
            self.data = self.data.sample(frac=1).reset_index(drop=True)
            self.data = self.data.sample(n=30)
            self.data.reset_index(drop=True, inplace=True)

    def initialize_centroids(self):
        idx = 0
        for cluster in self.clusters:
            self.centroids.append(idx)
            cluster.append(idx)
            idx += 1

    def clear_clusters(self):
        for cluster in self.clusters:
            cluster.clear()

    def calc_centroids(self):
        new_centroids = []
        idx = 0

        for cluster in self.clusters:
            if len(cluster) <= 2:
                new_centroids.append(self.centroids[idx])
            else:
                if idx not in self.dp:
                    distances = [[] for _ in range(len(cluster))]
                    for i in range(len(cluster)):
                        for j in range(len(cluster)):
                            distances[i].append(self.distance_calc.dis_for_clustering(
                                self.data.iloc[cluster[i]],
                                self.data.iloc[cluster[j]]))

                    self.dp[idx] = distances
                else:
                    distances = self.dp[idx]
                    distances.append([])
                    for i in range(len(cluster)):
                        dist = self.distance_calc.dis_for_clustering(
                            self.data.iloc[cluster[i]],
                            self.data.iloc[cluster[-1]])

                        distances[i].append(dist)
                        distances[-1].append(dist)

                scores = []
                for i in range(len(distances)):
                    scores.append(sum(distances[i]))

                new_centroids.append(cluster[np.argmin(scores)])

            idx += 1

        print(f"old: {self.centroids}, new: {new_centroids}")
        self.centroids = new_centroids

    def find_closest_cluster(self, entry, idx):
        distances = []

        print(f"now working with: {idx}")
        if idx in self.centroids:
            return None

        for centroid in self.centroids:
            distances.append(self.distance_calc.dis_for_clustering(entry, self.data.iloc[centroid]))

        return self.centroids[np.argmin(distances)]

    def add_to_cluster(self, centroid_idx, entry):
        for cluster in self.clusters:
            if centroid_idx in cluster:
                # print(f"SUCCESS- adding {entry}, to cluster: {cluster}")
                cluster.append(entry)
                break

        print(self.centroids)
        print(self.clusters)

    def fit(self):
        self.models = []
        self.initialize_centroids()
        # for i in range(self.max_iter):
        for idx, entry in self.data.iterrows():
            # print(f"now working on: {idx}")
            centroid_idx = self.find_closest_cluster(entry, idx)
            # print(centroid_idx)
            if centroid_idx is not None:
                self.add_to_cluster(centroid_idx, idx)
                self.calc_centroids()
                # self.centroids = new_centroids

                # self.centroids = self.compute_centroids(X, self.labels)
                # if np.all(new_centroids == self.centroids):
                #     break

        self.models.append((self.centroids, self.clusters))

    def predict(self, entry):
        return self.centroids[self.find_closest_cluster(entry)]


x = Kmeans('../../dataTool/clean_data/dataSet/test.json', 4, 10)
x.fit()
for model in x.models:
    my_print(model)