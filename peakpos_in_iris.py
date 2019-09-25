#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:46:47 2019
@author: yujijun
Description: This is a script to extract all chr22 peak pos in iris
Input: 
    /home/jjyu/DNase_summary/Input/04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv
Output:
    /home/jjyu/DNase_summary/Output

"""
import pandas as pd 
import numpy as np


#---------parameter-------------
Input_path = '/home/jjyu/DNase_summary/Input'
Output_path = '/home/jjyu/DNase_summary/Output'
Filter_name = '04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv'
#-----------------------------
Input_filter = pd.read_csv('%s/%s' %(Input_path, Filter_name), sep = ',')

All_chr22_pos = []
for i in range(len(Input_filter)):  
    print("This is processing the %d.th file!" %i)
    Summit_file = Input_filter.summit.tolist()[i]
    Input_summit = pd.read_csv('%s' %Summit_file, sep='\t',header=None)
    Input_allchr = Input_summit[0].tolist()
    Input_chr22_index = [i for i in range(len(Input_allchr)) if Input_allchr[i] == 'chr22']
    Input_chr22 = Input_summit.loc[Input_chr22_index,:]
    chr22_pos = Input_chr22[1].tolist()
    All_chr22_pos.extend(chr22_pos)
    All_chr22_pos_uni = np.unique(All_chr22_pos).tolist()
    All_chr22_pos_uni_sort = np.sort(All_chr22_pos_uni)

with open('%s/All_chr22_peakpos.csv' %Output_path, 'w') as f:
    for item in All_chr22_pos_uni_sort:
        f.write('%d\t' %item)
