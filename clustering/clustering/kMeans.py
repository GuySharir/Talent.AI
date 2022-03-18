import json

import numpy as np
import pandas as pd
from numpy.linalg import norm


class Kmeans:

    def __init__(self, dataPath: str, n_clusters: int, max_iter: int = 100, random_state: int = None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.data: pd.DataFrame = None
        self.load_data(dataPath)
        self.centroids = []
        self.clusters = [set() for _ in range(n_clusters)]

    def load_data(self, dataPath: str) -> pd.DataFrame:
        with open(dataPath, 'r') as file:
            json_data = json.load(file)
            self.data = pd.DataFrame.from_records(json_data)

    def initializ_centroids(self):
        self.data = self.data.sample(frac=1).reset_index(drop=True)
        centroid_idxs = np.random.randint(0, len(self.data), self.n_clusters)

        for idx in centroid_idxs:
            self.centroids.append(self.data.iloc[idx])

    def compute_centroids(self, X, labels):
        centroids = np.zeros((self.n_clusters, X.shape[1]))
        for k in range(self.n_clusters):
            centroids[k, :] = np.mean(X[labels == k, :], axis=0)
        return centroids

    def compute_distance(self, X, centroids):
        distance = np.zeros((X.shape[0], self.n_clusters))
        for k in range(self.n_clusters):
            row_norm = norm(X - centroids[k, :], axis=1)
            distance[:, k] = np.square(row_norm)
        return distance

    def find_closest_cluster(self, distance):
        return np.argmin(distance, axis=1)

    def compute_sse(self, X, labels, centroids):
        distance = np.zeros(X.shape[0])
        for k in range(self.n_clusters):
            distance[labels == k] = norm(X[labels == k] - centroids[k], axis=1)
        return np.sum(np.square(distance))

    def fit(self, X):
        # for i in range(self.max_iter):
        for entry in self.data.iterrows():
            old_centroids = self.centroids
            distance = self.compute_distance(X, old_centroids)
            self.labels = self.find_closest_cluster(distance)
            self.centroids = self.compute_centroids(X, self.labels)
            if np.all(old_centroids == self.centroids):
                break
        self.error = self.compute_sse(X, self.labels, self.centroids)

    def predict(self, X):
        distance = self.compute_distance(X, self.centroids)
        return self.find_closest_cluster(distance)


x = Kmeans("../../dataTool/clean_data/facebookEmployees.json", 5).initializ_centroids()
