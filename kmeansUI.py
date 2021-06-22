from pandas import DataFrame
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from mpl_toolkits import mplot3d


# GLOBAL VARIABLES
clusters = {}
centroids = []
df = {}



def getCSV():
    """
    Get the data.
    """
    global df
    global centroids

    # number of clusters
    try:
        numberOfClusters = int(entry1.get())

    except Exception as e:
        tk.messagebox.showerror(title="Clusters", message="Please enter the number of clusters")
        return

    else:
        import_file_path = filedialog.askopenfilename()

        try:
            read_file = pd.read_csv(import_file_path)
            df = pd.DataFrame(read_file, columns=['x', 'y'])

            tk.messagebox.showinfo(title="Success", message="Iterate to observe K-Means clustering")

        except Exception as e:
            print(e)
            tk.messagebox.showerror(title="Error", message="Unable to load CSV file. Try again")




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




def kMeans(data):
        
    """
    Performs K-means clustering.
    
    Parameters
    ----------
    data : ndarray or dataframe
    
    """

    global clusters
    
    global centroids


    if (type(data) == dict):
        tk.messagebox.showerror(title="Data Import", message="Please import your CSV data")
        return


    # if K > sample size, break 
    if (int(entry1.get()) > data.shape[0]):
        tk.messagebox.showerror(title='Inappropriate K', message='K cannot be greater than the sample size')
        return
    

        
    try:
        if len(centroids) == 0:
            random_numbers = list(set((random.randint(1, data.shape[0]) for i in range(10))))[:int(entry1.get())]
            centroids = [data.iloc[i].tolist() for i in random_numbers]
    except Exception as e:
        print(e)
        tk.messagebox.showerror(title="Data Import", message="Please import your CSV data")
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
        tk.messagebox.showinfo(title="Complete", message="Stopping condition has been reached: {}".format(centroids))
        plot_graph()
        return
    
    centroids = myCentroids
    tk.messagebox.showinfo(title='Cluster centers', message = "Centroids: {}".format(centroids))

    plot_graph()
    
    



def plot_graph():
    """Show clusters
    Plots three dimensions if the dataset is a three dimensional, otherwise
    it plots the first 2 dimensions.
    """

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




def restart():
    """Restart the clustering process."""
    global clusters
    global centroids
    global df

    clusters = {}
    centroids = []
    df = {}

    entry1.delete(0, tk.END)






# ===
# GUI
# ===
root = tk.Tk();
canvas1 = tk.Canvas(root, width = 400, height = 400, relief = "raised")
canvas1.pack()

label1 = tk.Label(root, text="K-Means Clustering")
label1.config(font=('helvetica', 20, 'bold'))
canvas1.create_window(200, 50, window=label1)

name = tk.Label(root, text="Developed by Mohammed Rashid, U1123916")
name.config(font=('helvetica', 15))
canvas1.create_window(200, 100, window=name)

# button to load excel data
browseButtonExcel = tk.Button(text=" Import CSV file ", command=getCSV, font=('helvetica', 10, 'bold'), padx=12, pady=9)
canvas1.create_window(200, 150, window=browseButtonExcel)

label2 = tk.Label(root, text="Enter the number of clusters")
label2.config(font=('helvetica', 18))
canvas1.create_window(200, 200, window=label2)

entry1 = tk.Entry(root)
canvas1.create_window(200, 250, window=entry1)
    
iterate = tk.Button(text=' Iterate ', command = lambda: kMeans(df), padx=12, pady=9, fg='green')
canvas1.create_window(200, 300, window=iterate)

restart = tk.Button(text=' Restart ', command= restart, padx=12, pady=9, fg='red')
canvas1.create_window(200, 350, window=restart)
        
    
root.mainloop();