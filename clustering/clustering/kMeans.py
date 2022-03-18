import json
import numpy as np
import pandas as pd
from numpy.linalg import norm
from program.DistanceFlow import DistanceFlow


class Kmeans:

    def __init__(self, dataPath: str, n_clusters: int, max_iter: int = 20, random_state: int = None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.data: pd.DataFrame = None
        self.load_data(dataPath)
        self.centroids = []
        self.clusters = [[] for _ in range(n_clusters)]
        self.distance_calc: DistanceFlow = DistanceFlow(False, False)

    def load_data(self, dataPath: str) -> pd.DataFrame:
        with open(dataPath, 'r') as file:
            json_data = json.load(file)
            self.data = pd.DataFrame.from_records(json_data)
            self.data = self.data.sample(frac=1).reset_index(drop=True)
            self.data = self.data.sample(n=30)

    def initialize_centroids(self):
        for idx, group in enumerate(self.clusters):
            self.centroids.append(idx)
            group.append(idx)

    def clear_clusters(self):
        for cluster in self.clusters:
            cluster.clear()

    def calc_centroids(self):
        # add caching for distance calcs
        # in order to reduce complexity

        new_centroids = []
        for idx, cluster in self.clusters:
            if len(cluster) <= 2:
                new_centroids.append(self.centroids[idx])
            else:
                distances = [[] for _ in len(cluster)]
                for i, a in enumerate(cluster):
                    for j, b in enumerate(cluster):
                        distances[i][j] = distances[j][i] = self.distance_calc.run_distance_flow(self.data.iloc[a],
                                                                                                 self.data.iloc[b])

                scores = []
                for i in range(len(distances)):
                    scores.append(sum(distances[i]))

                new_centroids.append(np.argmin(scores))

        return new_centroids

    def find_closest_cluster(self, entry):
        distances = []
        for centroid in self.centroids:
            distances.append(self.distance_calc.run_distance_flow(entry, self.data.iloc[centroid]))

        print(distances)
        return np.argmin(distances)

    def add_to_cluster(self, centroid_idx, entry):
        centroid = self.centroids[centroid_idx]

        res_cluster = None
        for cluster in self.clusters:
            if centroid in cluster:
                res_cluster = cluster
                break

        res_cluster.add(entry)

    # def compute_sse(self, X, labels, centroids):
    #     distance = np.zeros(X.shape[0])
    #     for k in range(self.n_clusters):
    #         distance[labels == k] = norm(X[labels == k] - centroids[k], axis=1)
    #     return np.sum(np.square(distance))

    def fit(self):
        self.models = []
        self.initialize_centroids()
        for i in range(self.max_iter):
            # self.initialize_centroids()
            self.clear_clusters()

            for idx, entry in enumerate(self.data.iterrows()):
                centroid_idx = self.find_closest_cluster(entry)
                self.add_to_cluster(centroid_idx, idx)
                new_centroids = self.calc_centroids()

                # self.centroids = self.compute_centroids(X, self.labels)
                if np.all(new_centroids == self.centroids):
                    break

            self.models.append((self.centroids, self.clusters))

    def predict(self, entry):
        return self.centroids[self.find_closest_cluster(entry)]


x = Kmeans('../../dataTool/clean_data/dataSet/test.json', 4, 10)

x.fit()

for model in x.models:
    print(model)
