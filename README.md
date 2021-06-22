# Use Instructions

## Prerequisites

### Install Python3
Prior to executing any of the ```*.py``` files in this folder, please make sure that Python 3 is installed on your computer. Click [here]("https://www.python.org/downloads/") to learn how to install Python 3. You may also prefer to have multiple versions of python running on your computer. In that case, click [here]("https://docs.python.org/3/library/venv.html") to learn how to create Python virtual environments.

### Install required packages

The packages required to successfully execute any ```*.py``` file are stored in the ***requirements.txt*** file. Run the following command to install all packages using the ```pip``` package manager.
```bash
pip install -r requirements.txt
```
 

## K-means Clustering
Perform the following tasks to visualize the operation of the K-means clustering algorithm. The algorithm uses the data in **sample.csv** to perform clustering. If you prefer to use your own dataset, please make sure your data has exactly two dimensions with label names, ***x*** and ***y***.

### Step 1:
Run the following code in the command line.
```bash
python3 kmeansUI.py
```

You should see the first screen of the K-means application
!["First screen of the k-means application"]("./Kmeans ui.png")
<img src="Kmeans ui.png">

### Step 2: 
Enter the number of clusters, *k*, in the input field.

### Step 3:
Upload the **sample.csv** file by clicking on the **Import CSV** button.

### Step 4:
Click on the **Iterate** button to visualize the operation of the K-means clustering. Keep clicking until the application notifies you that the stopping condition has been reached.
!["Stopping condition has been reached"]("Stopping condition.png")

<br/>

## The Apriori Algorithm
The apriori application uses the data in the **my_orders.csv** file. The file comprises of data about the order and product information from The Instacart Online Grocery Shopping Dataset 2017. The ***order_id*** is a unique 1-digit code for a transaction whereas the ***product_id*** is a unique 5 digit code for a product.  Perform the following tasks to visually inspect how the aprior algorithm works.

### Step 1:
Run the following command in the command line
```bash
python3 apriori-UI.py
```

You should see the first screen of the application.
["First screen of the apriori application"]("First apriori.png")

### Step 2:
Click on the **Iterate** button to see apriori in action. Keep clicking on the button until the algorithm converges.
["Apriori converged"]("Converged.png")








