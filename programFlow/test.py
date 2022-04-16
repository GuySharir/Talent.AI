import os
import pickle
import sys
from kMeans import Kmeans

import pandas as pd  # dataframe manipulation
import numpy as np  # linear algebra

# data visualization
import matplotlib.pyplot as plt
from yellowbrick.cluster import KElbowVisualizer  # cluster visualizer

# sklearn kmeans
from sklearn.cluster import KMeans
from sklearn.metrics.cluster import contingency_matrix

from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import random_center_initializer
from pyclustering.cluster.encoder import type_encoding
from pyclustering.cluster.encoder import cluster_encoder
from pyclustering.utils.metric import distance_metric, type_metric
from DistFunctions import prepare_data_for_dist_calc_between_freq_vectors


def elbow(data):
    # Instantiate the clustering model and visualizer
    model = KMeans()
    visualizer = KElbowVisualizer(model, k=(1, 11))

    visualizer.fit(data)  # Fit the data to the visualizer
    visualizer.show()  # Finalize and render the figure
    plt.show()


def skLearn(data):
    # instatiate KMeans class and set the number of clusters
    km_model = KMeans(n_clusters=4, random_state=10)

    # call fit method with data
    km = km_model.fit_predict(data)

    # coordinates of cluster center
    centroids = km_model.cluster_centers_

    # cluster label for each data point
    labels = km_model.labels_

    # purity = purity_score(y, labels)
    # print(f"The purity score is {round(purity * 100, 2)}%")


# def purity_score(y_true, y_pred):
#     # compute contingency matrix (also called confusion matrix)
#     confusion_matrix = contingency_matrix(y_true, y_pred)
#     # return purity
#     return np.sum(np.amax(confusion_matrix, axis=0)) / np.sum(confusion_matrix)

# Report Purity Score


def pyPurity(data):
    metric = distance_metric(type_metric.USER_DEFINED, func=prepare_data_for_dist_calc_between_freq_vectors)

    # initial_centers = random_center_initializer(data, 4, random_state=10).initialize()
    # instance created for respective distance metric
    instanceKm = kmeans(data, initial_centers=[data.iloc[0], data.iloc[1], data.iloc[2], data.iloc[3]], metric=metric)
    # perform cluster analysis
    instanceKm.process()
    # cluster analysis results - clusters and centers
    pyClusters = instanceKm.get_clusters()
    pyCenters = instanceKm.get_centers()
    # enumerate encoding type to index labeling to get labels
    pyEncoding = instanceKm.get_cluster_encoding()
    pyEncoder = cluster_encoder(pyEncoding, pyClusters, data)
    pyLabels = pyEncoder.set_encoding(0).get_clusters()
    # function purity score is defined in previous section
    # return purity_score(y, pyLabels)
    return pyLabels


print("here")
with open('../model.pkl', 'rb') as inp:
    model = pickle.load(inp)
    # elbow(model.data)
    print(model.data)
    x = pyPurity(model.data.reset_index())
    print(x)

print("done")
