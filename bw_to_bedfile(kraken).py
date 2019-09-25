#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:46:47 2019
@author: yujijun
Description: This is a script to convert file from bigwig to bedfile in kraken.
we can choose different chromosome and resolution to generate different bigwig file.
Input: 
    /homes/jjyu/higlass_projects/Input/DNase_bw_v1/*
Output:
    /homes/jjyu/higlass_projects/Output/1308_manysample


Output: 
01-Homo_sapiens_ca_DNase.csv 
02-Homo_sapiens_ca_DNase_QC(906).txt
"""

import pyBigWig
import numpy as np
import pandas as pd 
import math
#--------------hyperparameter--------------------
basic_path = '/homes/jjyu/higlass_projects'
Input_path = '%s/Input/DNase_bw_v1' %basic_path
Output_path = '%s/Output/higlass_543_16'
filter_data = pd.read_csv('%s/04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv' % Output_path,sep=",")
resolution = 16
length_chr22 = 50818468
#--------------------------------------------

#Firsthalf
df_Firsthalf_empty = pd.DataFrame(columns=["chr_name", "start", "end"])
df_Firsthalf_empty.chr_name = ["chr22"] * math.ceil(length_chr22/resolution)
df_Firsthalf_empty.start = np.arange(0,length_chr22,resolution)
df_Firsthalf_empty.end = np.append(np.arange(resolution,length_chr22,resolution),length_chr22)

#lasthalt_empty
list_str = [str(i+1) for i in range(len(filter_data))]
columns_list = ["value"+i for i in list_str]
df_lasthalf_empty = pd.DataFrame(columns = columns_list)

#defind a normalization function
def normalization(x):
    Whole_mean = sum(x)/len(x)
    newList = [xi / Whole_mean for xi in x]
    return(newList)

#filter_data.DatsetID = [1,6]
m = 0
for i in range(len(filter_data.DatsetId)):
    print("This is %s .th file." %(i+1) )
    #input_folder = 'dataset' + str(filter_data.DatsetId[i])
    input_name = str(filter_data.DatsetId[i]) + "_" + "treat.bw"
    input_file = '%s/%s' %(Input_path, input_name)
    print(input_file)
    try:
        bw = pyBigWig.open(input_file)
    except RuntimeError:
        print("This is a error file.")
        continue
    if ('chr22' in bw.chroms().keys()):
        chr22_values = bw.values("chr22",0,bw.chroms('chr22'))
        chr22_values_split16 = [chr22_values[i:i + resolution] for i in range(0, len(chr22_values), resolution)]
        chr22_values_split16_mean = [np.mean(x) for x in chr22_values_split16]
        chr22_values_split16_mean_norm = normalization(chr22_values_split16_mean)
        df_lasthalf_empty.iloc[:,m] = chr22_values_split16_mean
        m +=1
        bw.close()
        print("\t")

#concat two dataframe
df_merge = pd.concat([df_Firsthalf_empty, df_lasthalf_empty], axis=1)
df_merge.to_csv('%s/bedfile_16_543.csv' %Output_path, sep='\t',index=False, header=True)
