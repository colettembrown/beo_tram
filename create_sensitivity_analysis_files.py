import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os


def fill_missing_labels(data, m, n):
    '''
    Fills missing values for a specific polygon feature (m) in the projected data by sampling from the values of another label (n).

    Args: 
        Data (DataFrame): a four-column DataFrame with the pre-existing data
        m: label that needs to be filled
        n: label from which values for 'm' will be sampled

    Returns:
        pd.DataFrame: The df with missing values for label 'm' filled
    '''

    rows_to_fill = data.iloc[:,2] == m
    rows_to_sample = data.iloc[:,2] == n

    sample_values = data.loc[rows_to_sample, "Var4"].dropna().values

    num_to_fill = rows_to_fill.sum()
    sampled_values = np.random.choice(sample_values, size=num_to_fill, replace=True)
    
    data.loc[rows_to_fill, 3] = sampled_values

    return data



polygon_types = {
    1: 'Trough & LCP',
    2: 'Trough & FCP',
    3: 'Trough & HCP',
    4: 'Center & LCP',
    5: 'Center & FCP',
    7: 'High & LCP',
    8: 'High & FCP',
    9: 'High & HCP'
}



path_to_projections = "/Users/colettebrown/Library/CloudStorage/GoogleDrive-coletteb@berkeley.edu/Shared drives/Tram/data/projections/"
group_order = ['spring_snow_', 'spring_transition_', 'spring_no_snow_', 'peak_NDVI_']
variables = ['Albedo']
years = ['2014', '2015', '2016', '2017']

for group in group_order:
    for variable in variables:
        file_pattern = os.path.join(path_to_projections, f"{group}{variable}_*.txt")
        for file in glob.glob(file_pattern):
            file_name = os.path.basename(file)
            year = file_name[-8:-4]
            
            df = pd.read_csv(file)
            
            # resampling if HCP = LCP
            resample_trough_LCP = fill_missing_labels(df, m=3, n=1)
            resample_high_LCP = fill_missing_labels(df, m=9, n=7)
            resample_high_LCP.to_csv(f'data/LCP_sensitivity_{group}{variable}_{year}.csv', header=True, index=False)

            # resampling if HCP = FCP
            resample_trough_FCP = fill_missing_labels(df, m=3, n=2)
            resample_high_FCP = fill_missing_labels(df, m=9, n=8)
            resample_high_FCP.to_csv(f'data/FCP_sensitivity_{group}{variable}_{year}.csv', header=True, index=False)
            
            