# -*- coding: utf-8 -*-
#AHA! Python for Data Analytics
#PA Starter Code
#@author: gsprint

import sys
import random
import pandas as pd

######################################
# PROVIDED CLASS AND FUNCTIONS
######################################    
class Cluster:
    '''
    represents a cluster in k-means clustering
    stores the samples belonging to the cluster in a dataframe
    the centroid of the cluster is computed as needed by compute_prototype()
    '''
    def __init__(self, df=None):
        '''
        constructor
        df is data frame
        '''
        self.df = df
        
    
    def __str__(self):
        '''
        return a string representation of the cluster
        returning the clusters prototype and number of samples
        '''
        return "Prototype: \n%s\nNum Samples: %d\n" %(str(self.compute_prototype()), len(self.df))
        
    def add_sample(self, sample): 
        '''
        add a sample to this cluster's data frame
        '''
        self.df = self.df.append(sample)
        
    def compute_prototype(self):
        '''
        compute the prototype by taking the average of the samples
        '''
        if len(self.df) > 0:
            return self.df.mean(axis=0)
        else:
            return None

def display_clusters(clusters):
    '''
    utility function to display the data frame and prototype of each cluster
    '''
    for i, cluster in enumerate(clusters):
        print("Cluster:", i)
        print(cluster.df)
        print(cluster)        
      
def create_empty_clusters(k, columns):
    '''
    k is the number of clusters
    columns is a list of feature labels
    '''
    clusters = []
    # create k empty clusters
    for i in range(k):
        cluster = Cluster(pd.DataFrame(columns=columns))
        clusters.append(cluster)
    return clusters
    
def randomly_assign_to_clusters(k, df, clusters):
    '''
    k is the number of clusters
    df is the data frame containing the samples to assign to clusters
    clusters is the list of Cluster objects to assign samples to
    '''
    # ensure each cluster gets at least one sample
    for i in range(k):
        sample = df.iloc[i]
        cluster = clusters[i]
        cluster.add_sample(sample)
        
    # initialization: randomly assign samples to each cluster
    for i in range(k, len(df.index)):
        sample = df.iloc[i]
        cluster_index = random.randrange(0, k)
        cluster = clusters[cluster_index]
        cluster.add_sample(sample)
   
######################################
# TODO: Finish main() and add functions
######################################
def main():
    '''
    Example runs
    files\simple.csv files\simple_results.csv 3 5
    files\cancer.csv files\cancer_results.csv 2 5
    '''
    if len(sys.argv) == 5:
        input_fname = sys.argv[1]
        output_fname = sys.argv[2]
        k = int(sys.argv[3]) 
        max_iterations = int(sys.argv[4])
    else:
        print("Usage: input_filename output_filename K max_iterations" + 
              "\nExample: files\\simple.csv files\\simple_results.csv 3 5")
        sys.exit(-1)
        
    # seed the random number generator with a constant
    random.seed(1)
    df = pd.read_csv(input_fname, index_col=0, header=None)
    print("Data frame shape:", df.shape)
    
    clusters = create_empty_clusters(k, df.columns)
    randomly_assign_to_clusters(k, df, clusters)
    display_clusters(clusters)
    # TODO: Implement K means clustering 
    # TODO: write out cluster results
    
if __name__ == "__main__":
    main()