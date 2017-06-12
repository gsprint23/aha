# -*- coding: utf-8 -*-
#AHA! Activity Change Detection
#PA Starter Code
#@author: gsprint

import pandas as pd
import numpy as np
from collections import OrderedDict
import os
import sys


######################################
# PROVIDED FUNCTIONS
######################################    
def build_daily_steps_df(data_dir):
    '''
    data_dir is the unzipped directory containing all of the csv files
    returns a data frame containing time series step data for each day
    '''
    intraday_files = OrderedDict()
    for (dirpath, dirnames, filenames) in os.walk(data_dir):
        for fil in filenames:
            parts = fil.split("_")
            day = parts[1][:10]
            relative_path = data_dir + "\\" + fil
            day_df = pd.read_csv(relative_path, header=0, parse_dates={"time": [0]})
            day_df.set_index("time", inplace=True)
            intraday_files[day] = day_df
    day1 = list(intraday_files.keys())[0]
    # be aware that this removes a key-value pair from the dictionary each time it executes
    day1_df = intraday_files.pop(day1)
    day1_steps_ser = day1_df["steps"]
    day1_steps_ser.name = day1 # instead of "steps"
    all_df = pd.DataFrame(day1_steps_ser)
    for day, df in intraday_files.items():
        all_df[day] = df["steps"]   
    return all_df
 
def compute_features_df(df, mins_interval):
    '''
    df is the time series steps data frame
    mins_interval is the number of minutes per interval the data was re-sampled to
    use mins_interval parameter to support re-sampling
    '''
    features_df = pd.DataFrame(index=df.columns)
    features_df["total"] = df.sum()
    features_df["max"] = df.max()
    features_df["mean"] = df.mean()
    features_df["std"] = df.std()

    # PHYSICAL ACTIVITY INTENSITY FEATURES
    intensities = ["sedentary", "low", "moderate", "high"]
    # add blank columns for each intensity. values will be filled in one at a time
    for intensity in intensities:
        features_df[intensity] = np.NaN
        
    # the largest step count in the data set
    max_val = df.max().max()
    # exclusive of left, inclusive of right
    # TODO: modify bins to support resampled data
    bins = [-1, 4, 39, 99, max_val]

    for date in df.columns:
        intensity_ser = pd.cut(df[date], bins, labels=intensities)
        counts = pd.value_counts(intensity_ser)
        for intensity in intensities:
            percentage = counts.loc[intensity] / len(df.index) * 100
            features_df.ix[date][intensity] = percentage
    return features_df

######################################
# TODO: Finish main() and add functions
######################################
def main():
    '''
    example runs
    files\fitbit_example2_data files\aha-ds_60_features.csv files\aha-ds_60_b.csv 60 b
    resampled to 60 minutes, baseline comparisons
    
    files\fitbit_example2_data files\aha-ds_15_features.csv files\aha-ds_15_s.csv 15 s
    resampled to 15 minutes, sliding comparisons
    '''
    if len(sys.argv) == 6:
        data_dir = sys.argv[1]
        features_file = sys.argv[2]
        results_file = sys.argv[3]
        t_mins = int(sys.argv[4])    
        mode = sys.argv[5]
    else:
        print("Usage: data_directory features_file_name results_file_name t_mins mode" + 
              "\nExample: files\\fitbit_example2_data files\\aha-ds_60_features.csv files\\aha-ds_60_b.csv 60 b")
        sys.exit(-1)
          
    steps_df = build_daily_steps_df(data_dir)
    # resample the data by summing
    df = steps_df.resample(str(t_mins) + "T").sum()
    features_df = compute_features_df(df, t_mins)
    # write the resampled data features to a file
    features_df.to_csv(features_file)
    
    # TODO: call appropriate function for baseline or sliding comparisons based on mode
    # TODO: write out change score results
    
if __name__ == "__main__":
    main()