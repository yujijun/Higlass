#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 08:02:41 2019
@author: yujijun
Description: This is a script to generate bedfile by peak

Input: 
    /homes/jjyu/higlass_projects/Output/higlass_543_16
    /homes/jjyu/higlass_projects/Input/All_chr22_peakpos.csv
Output:
    /homes/jjyu/higlass_projects/Output/higlass_peak_16_543
    
"""
import pandas as pd 
import numpy as np
import math
import time 
from collections import Counter
import matplotlib.pyplot as plt 
import matplotlib
import random
from scipy.cluster.hierarchy import dendrogram, linkage,fcluster
import warnings
warnings.filterwarnings("ignore")

#--------------------hyperparameter--------------------
basic_path = '/homes/jjyu/higlass_projects'
Input_path = '%s/Input' %basic_path
Output_path = '%s/Output' %basic_path

peak_pos_name = '%s/All_chr22_peakpos.csv' %Input_path
bedfile_name = '%s/higlass_543_16/bedfile_16_543.csv' %Output_path
resolution = 16
#-------------------------------------------------------
peakpos = pd.read_csv(peak_pos_name, sep = '\t', header=None, index_col=None)
bedfile = pd.read_csv(bedfile_name, sep = '\t')     

peakpos_list = [int(i) for i in peakpos.iloc[0:].values.tolist()[0] if (math.isnan(i) != True)]

#v0
start_time = time.time()
index_v1_0 = []
for i in range(len(peakpos_list)):
    pos_fold = int(np.floor(peakpos_list[i]/resolution))
    if peakpos_list[i]%resolution == 0:
        index_v1_0.append(pos_fold-1)
    else:
        index_v1_0.append(pos_fold)
index_v1_0 = np.unique(index_v1_0)
end_time = time.time()
print(end_time - start_time)   

bedfile_peak = bedfile.iloc[index_v1_0,:]

output_name = '%s/bedfile_peak_16_543.csv' %Output_path
bedfile_peak.to_csv('%s/%s' %(Output_path, output_name), sep='\t', header=None, index=None)

#choose all samples values and delete the row which all values of samples is zero 
#bedfile_peak_samples = bedfile_peak.iloc[:,3:]
#bedfile_peak_first = bedfile_peak.iloc[:,0:3]
#bedfile_peak_samples_del0 = bedfile_peak_samples.loc[(bedfile_peak_samples.sum(axis=1) != 0),(bedfile_peak_samples.sum(axis=0) != 0)]
