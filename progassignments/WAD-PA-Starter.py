# -*- coding: utf-8 -*-
#AHA! Working with Activity/Health Data
#PA Starter Code
#@author: gsprint

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ric_decoder = {1: "Stroke", 2: "TBI", 3: "NTBI", 4: "TSCI", 5: "NTSCI", 6: "Neuro",
     7: "FracLE", 8: "ReplLE", 9: "Ortho", 10: "AMPLE", 11: "AMP-NLE", 12: "OsteoA",
     13: "RheumA", 14: "Cardiac", 15: "Pulmonary", 16: "Pain", 17: "MMT-NBSCI",
     18: "MMT-BSCI", 19: "GB", 20: "Misc", 21: "Burns"}

######################################
# PROVIDED FUNCTIONS
######################################         
def read_in(fname):
    df = pd.read_csv(fname, header=0, index_col=0)
    return df
    
def plot_histogram(name, fname, x, x_label):
    '''
    
    '''
    mu = np.mean(x)
    sigma = np.std(x)
    fig, ax = plt.subplots()
    # TODO: call hist() to plot the histogram
    # TODO: call mlab.normpdf() and plot() to plot the normal curve approximation
    
    plt.xlabel(x_label)
    plt.ylabel('Frequency')
    title = '%s (N=%d): $ \mu=%.2lf,\ \sigma=%.2lf$' %(name, len(x), mu, sigma)
    plt.title(title)
    plt.savefig(fname)  
    plt.close("all")     
    
def generate_histogram_plots(df, out_dir):
    '''
    
    '''
    rics = df.groupby("RIC")
    for ric, group_df in rics:
        ric = str(ric) # before cleaning, RIC is an integer
        age = group_df["Age"]
        if len(age) > 2:
            fname = out_dir + "\\" + ric + "_age.png"
            plot_histogram(ric + " Age", fname, age, "Age (years)")
            
def plot_scatter(name, fname, fimA, fimD, genders):
    '''
    
    '''
    fig, ax = plt.subplots()
    # TODO: Grab the male and female data frames from genders 
    # TODO: Add 2 calls to scatter(), one for males and one for females
    lims = [0.0, 140.0]
    
    # plotting y = x
    nochange, = ax.plot(lims, lims, color='black', lw=3.0, ls='--', label="No Change")
    ax.legend(loc=4)
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_xlabel(fimA.name)
    ax.set_ylabel(fimD.name)
    ax.set_title(name + " (N=%d)" %(len(fimA)))
    plt.savefig(fname)
    plt.close("all")
        
def generate_scatter_plots(df, out_dir):
    '''
    
    '''
    rics = df.groupby("RIC")
    for ric, group_df in rics:
        ric = str(ric) # before cleaning, RIC is an integer
        fimA = group_df["Admission Total FIM Score"]
        fimD = group_df["Discharge Total FIM Score"]
        genders = group_df.groupby("Gender")
        if len(genders) > 1:
            fname = out_dir + "\\" + ric + "_fim.png"
            plot_scatter(ric, fname, fimA, fimD, genders)

######################################
# TODO: Finish main() and add functions
######################################
def main():
    '''
    Example run
    files\patient_data_to_clean.csv files\patient_data_cleaned.csv files\patient_data_stats.csv figures\patient_age_histograms figures\patient_fim_scatters
    '''
    if len(sys.argv) == 6:
        fname = sys.argv[1]
        cleaned_fname = sys.argv[2]
        stats_fname = sys.argv[3]
        histo_dir = sys.argv[4]    
        scatter_dir = sys.argv[5]
    else:
        print("Usage: data_file_name cleaned_file_name stats_file_name histogram_directory scatter_directory" + 
              "\nExample: files\\patient_data_to_clean.csv files\\patient_data_cleaned.csv " + 
              "files\\patient_data_stats.csv figures\\patient_age_histograms figures\\patient_fim_scatters")
        sys.exit(-1)
        
    df = read_in(fname)
    print("Data frame shape:", df.shape)
    
    # TODO: add cleaning function calls
    # TODO: write out cleaned data frame
    # TODO: add code to compute and write out stats

    generate_histogram_plots(df, histo_dir)
    generate_scatter_plots(df, scatter_dir)
    
if __name__ == "__main__":
    main()