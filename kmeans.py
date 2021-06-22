from pandas import DataFrame
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import datetime as dt
import seaborn as sns

clusters = {}
centroids = []



# =================
# HELPER FUNCTIONS
# =================

def StandardScaler(series):
    """
    Performs Z-score normalisation
    
    Parameters
    -----------
    series: pd.core.series.Series
    
    
    Returns
    --------
    z: pd.core.series.Series
    Normalised measures
    """
    if type(series) == pd.core.series.Series:
        mean = series.mean()
        std = series.std()
        z = (series - mean)/std
        
    return z


def compute_centroids(vecOfVectors):
    """
    Calculates the centroid of a cluster
    
    Parameters
    -----------
    vecOfVectors: ndarray
    Array of points
    
    
    Returns
    -------
    Mean of the points
    """
    vectorArray = np.array(vecOfVectors)
    
    return np.round(np.mean(vectorArray, axis=0), 2)



def get_cluster_number(vector):
    """
    Find the cluster that an observation belongs to
    
    Parameters
    ----------
    vector : ndarray
    
    Returns
    -------
    The cluster number of a point
    
    """
    global centroids
    
    distances = np.sqrt(np.sum((np.array(vector) - centroids)**2, axis=1))
    
    # get the cluster number
    minimum_distance = min(distances)
    
    
    return distances.tolist().index(minimum_distance) + 1



def kMeans(data, k, max_iterations=500):
    
    """
    Performs K-means clustering.
    
    Parameters
    ----------
    data : ndarray or dataframe
    
    """
    global clusters
    global centroids

    

    
    for i in range(max_iterations):
        try:
            if len(centroids) == 0:
                random_numbers = list(set((random.randint(1, data.shape[0]) for i in range(10))))[:k]
                centroids = [data.iloc[i].tolist() for i in random_numbers]
        except Exception as e:
            print(e)
            print("Please import your CSV data")
            return


        myCentroids = []

        # initialise the clusters
        for i in range(np.array(centroids).shape[0]):
            clusters[i + 1] = []

        # for each point, find the cluster it belongs to
        for i in range(data.shape[0]):
            cluster_number = get_cluster_number(np.array(data.iloc[i]))

            # add it to the clusters        
            clusters[cluster_number].append(list(data.iloc[i])) 

        # update the centroids after cluster assignment   
        for i in clusters.keys():
            myCentroids.append(compute_centroids(clusters[i]).tolist())

        # stopping condition
        if(myCentroids == centroids):
            break;
        

        centroids = myCentroids

    plot_graph()
    
    
    
def plot_graph():
    """Show clusters"""

    if (np.array(centroids).shape[1] == 3):    
        ax = plt.axes(projection="3d")
        for i, key in enumerate(clusters.keys()):
            cluster = np.array(clusters.get(key))
            ax.scatter3D(cluster[:, 0], cluster[:, 1], cluster[:, 2])
            
            # Plot the centroids
            ax.scatter3D(np.array(centroids)[i, 0], np.array(centroids)[i, 1], np.array(centroids)[i, 2], marker="x", s = 150)
            ax.set_title("K-means clustering in action")
        

        plt.show()
        return;
        
    for i, key in enumerate(clusters.keys()):
        cluster = np.array(clusters.get(key))
        plt.scatter(cluster[:, 0], cluster[:, 1])
        plt.scatter(np.array(centroids)[i, 0], np.array(centroids)[i, 1], marker="x", s=20)
        plt.title("K-Means Clustering in Action")

    plt.show()



# Test the algorithm
df = pd.read_csv('rfm.csv', header=0)
kMeans(df, 3)