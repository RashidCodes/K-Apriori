import numpy as np
import pandas as pd
from itertools import combinations, groupby
from collections import Counter
from tkinter import * 

# =======================
# APRIORI SIDE OF THINGS
# =======================

# read in the data
my_orders = pd.read_csv("my_orders.csv")
my_orders = my_orders.set_index('order_id')['item_id']


# GLOBAL VARIABLES
k_itemset = 1
prune = False
frequent_itemsets = {}
final_itemset = {}

# candidate and final sets after every iteration
candidate = {}
final = {}

# termination condition
termination = False



# =================
# HELPER FUNCTIONS
# ================
def store_itemsets(df): 
    """
    Stores frequent itemsets in a hashmap

    Parameters
    ----------
    df : pd.DataFrame
    Dataframe containing itemsets and their support
    """
    global frequent_itemsets
    for index in df.index:
        frequent_itemsets[index] = float(df.loc[[index]]['support'])




def freq(item):
    """
    Count the number of times items (usually itemsets) occur

    Parameters
    ----------
    item: pd.core.series.Series, array-like
    An array of items
    

    Returns
    -------
    Counts of itemsets/items: int

    """
    if type(item) == pd.core.series.Series:
        return item.value_counts().rename("freq")
    
    else:
        return pd.Series(Counter(item)).rename("freq")
    
    
    

def order_count(orders):
    """
    Get the number of transactions in a dataset
    
    Parameters
    -----------
    orders: pd.Dataframe
    Order information

    Returns
    -------
    Total number of unique orders or transactions: int
    """
    return len(set(orders.index))




def get_itemset_without_prune(orders, k):

    """
    Get itemsets without pruning.

    Parameters
    -----------
    orders: pd.core.series.Series

    Yields
    ------
    Item_set: tuple
    A k-item set

    """
    
    orders = np.transpose(np.array([orders.index, orders]))
    
    for order_id, order_object in groupby(orders, lambda x:x[0]):
        item_list = [item[1] for item in order_object]
        
        for item_set in combinations(item_list, k):
            yield(item_set)
    




def get_itemset_with_prune(orders, k):
    """
    Get itemsets with pruning.

    Parameters
    -----------
    orders: pd.core.series.Series

    Yields
    ------
    Item_set: tuple
    A k-item set

    """
    orders = np.transpose(np.array([orders.index, orders]))
    
    
    
    for order_id, order_object in groupby(orders, lambda x:x[0]):
        item_list = [item[1] for item in order_object]
        
        
        for item_set in combinations(item_list, k):
            list_of_bools = []
            
            for subset in combinations(item_set, k-1):
                if frequent_itemsets.get(subset) == None:
                    list_of_bools.append(False)
                else:                    
                    list_of_bools.append(True)
                    
            
            if all(list_of_bools) == True:  
                yield(item_set)
    




def compute_parameters(itemset):
    """
    Compute the metrics of an association rule

    Parameters
    ----------
    itemset: pd.DataFrame
    A frequent itemset (has to be in the hashmap)


    Returns
    -------
    dataframe: pd.DataFrame
    Dataframe of association rules and their metrics
    """
    confidences = []
    rules = []
    lifts = []
    item_set = itemset.index.tolist()

    for item in item_set:
        # create subsets of the item
        for i in range(len(item) - 1):
            for subset in combinations(item, i + 1):
                confidence = frequent_itemsets.get(item) / frequent_itemsets.get(subset)
                rule = "{} -> {}".format(subset, item)
                lift = (frequent_itemsets.get(item)/100) / compute_lift(item)
                confidences.append(round(confidence, 2))
                rules.append(rule)
                lifts.append(round(lift, 2))
                
                
    return pd.DataFrame({'rules': rules, 'confidence': confidences, 'lift':lifts })

                
                
                
def compute_lift(items):
    """
    Utility function for computing the lift. It is used to compute support(A) * support(B) * support(C) *...

    Parameters
    ----------
    items: tuple

    Returns
    -------
    mul : float

    """

    mul = 1
    
    for product in items:
        mul *= frequent_itemsets.get((product,))/100
        
    return mul   



def produce_candidate(orders, k_items):
    """ 
    Produce a candidate set with pruning

    Parameters
    ----------
    orders: pd.core.series.Series
    
    k_items: int
    Length of itemsets in the candidate set


    Returns
    -------
    item_set_c1: pd.DataFrame
    Candidate set

    """
    
    candidate_gen = get_itemset_with_prune(orders, k_items)
    item_set_c1 = freq(candidate_gen).to_frame('freq')
    item_set_c1['support'] = item_set_c1['freq'] / order_count(orders) * 100
    
    return item_set_c1


def produce_candidate_without_prune(orders, k_items):
    """ 
    Produce a candidate set without pruning

    Parameters
    ----------
    orders: pd.core.series.Series
    
    k_items: int
    Length of itemsets in the candidate set


    Returns
    -------
    item_set_c1: pd.DataFrame
    Candidate set

    """
    candidate_gen = get_itemset_without_prune(orders, k_items)
    item_set_c1 = freq(candidate_gen).to_frame('freq')
    item_set_c1['support'] = item_set_c1['freq'] / order_count(orders) * 100
    
    return item_set_c1



def produce_final(candidate, support_thresh=40):
    """
    Produce final frequent itemsets from a candidate set.
    
    Parameters
    ----------
    candidate: pd.DataFrame
    
    support_thresh: int
    Support threshold
    
    
    Outputs
    --------
    item_set_f1: pd.DataFrame
    Final dataset
    
    """
    
    item_set_f1 = candidate[candidate['support'] >= support_thresh]
    
    return item_set_f1




# update text after each iteration
def clear_text():
    """
    Clear text inputs
    """
    global txt
    global txt2

    txt.delete("1.0", "end")
    txt2.delete("1.0", "end")


def update_text():
    """Update text inputs"""
    global txt

    global txt2

    if termination:
        txt.insert(END, "Algorithm converged")
        txt2.insert(END, "Algorithm converged")
        return;

    txt.insert(END, candidate)
    txt2.insert(END, final)





# Apriori algorithm
def apriori(support_thresh=40):
    """The Apriori algorithm
    
    Demonstrates the apriori algorithm with an example

    Parameters
    -----------
    support_thresh: int
    
    """
    
    global my_orders
    
    global prune
    
    global k_itemset
    
    global final_itemset

    global candidate

    global final

    global termination

    # update the gui, and put in the data
    clear_text();
    
    if(prune == False):
        c1 = produce_candidate_without_prune(my_orders, k_itemset)
        f1 = produce_final(c1)
        my_orders = my_orders[my_orders.isin(f1.reset_index().set_index('level_0').index)]
        
        print("Candidate for {}-itemsets".format(k_itemset))
        print(c1)
        
        print("Final for {}-itemsets".format(k_itemset))
        print(f1)
        # Let the prunning begin
        prune = True
    
        # maintain the previous final itemset    
        final_itemset = f1

        # store the frequent itemsets
        store_itemsets(f1)

        # increase the itemset
        k_itemset = k_itemset + 1

        candidate = c1
        final = f1

        # update the content of the text fields
        update_text()
        
        return
        
    
    c1 = produce_candidate(my_orders, k_itemset)
    candidate = c1
    
    print("Candidate for {}-itemsets".format(k_itemset))
    print(c1)
    
    f1 = produce_final(c1)
    final = f1

    print("Final for {}-itemsets".format(k_itemset))
    print(f1)

    # update the content of the text fields
    update_text()
    
    
    if f1.shape[0] == 0:
        termination = True;
        clear_text();
        update_text()
        return;
        

    
    # maintain the previous final itemset    
    final_itemset = f1
    
    # store the frequent itemsets
    store_itemsets(f1)
        
    # increase the itemset
    k_itemset = k_itemset + 1
    

    
    

# ====
# GUI
# ====
root = Tk()
root.geometry('400x950')

# Label
label = Label(root, text="The Apriori Algorithm", font=("Helvetica", 25), justify=CENTER, height=3)
label.pack()

label = Label(root, text="Developed by Mohammmed Rashid, U1123916", font=("Helvetica", 15), justify=CENTER)
label.pack()


label = Label(root, text="Candidate Set", font=("Helvetica", 20), justify="left", fg='red', height=5)
label.pack()

txt = Text(root, height=20, width=35)
txt.pack(pady=10) 


label = Label(root, text="Final Set", font=("Helvetica", 20), anchor=W, fg='green')
label.pack()

txt2 = Text(root, height=20, width=35)
txt2.pack(pady=10)



# iterate button
iterate = Button(text="Iterate", command=apriori, padx=12, pady=9, fg='green' )
iterate.pack()


print ("Candidate: ", candidate)

mainloop()