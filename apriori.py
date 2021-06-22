import numpy as np
import pandas as pd
from itertools import combinations, groupby
from collections import Counter


# read in the data
my_orders = pd.read_csv("my_orders.csv")
my_orders = my_orders.set_index('order_id')['item_id']

k_itemset = 1
prune = False
frequent_itemsets = {}
final_itemset = {}

# =================
# HELPER FUNCTIONS
# =================

# Association rules function
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
    Produce frequent itemsets
    
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




def apriori(support_thresh=40, max_iterations=50):
    """The Apriori algorithm


    Parameters
    -----------
    support_thresh: int
    The minimum support threshold
    
    max_iterations: int
    The number of times the algorithm should run.
    
    """
    global my_orders
    
    global prune
    
    global k_itemset
    
    global final_itemset
    

    for i in range(max_iterations):
        
        if(prune == False):
            c1 = produce_candidate_without_prune(my_orders, k_itemset)
            f1 = produce_final(c1)
            my_orders = my_orders[my_orders.isin(f1.reset_index().set_index('level_0').index)]

        
            # Let the prunning begin
            prune = True

            # maintain the previous final itemset    
            final_itemset = f1

            # store the frequent itemsets
            store_itemsets(f1)

            # increase the itemset
            k_itemset = k_itemset + 1

            continue

            
        c1 = produce_candidate(my_orders, k_itemset)
        f1 = produce_final(c1)
        

        if f1.shape[0] == 0:
            print("Association Rules\n------------------")
            print()
            print(compute_parameters(final_itemset))
            break;



        # maintain the previous final itemset    
        final_itemset = f1

        # store the frequent itemsets
        store_itemsets(f1)

        # increase the itemset
        k_itemset = k_itemset + 1    
    


apriori();