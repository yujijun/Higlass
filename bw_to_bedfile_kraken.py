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

"""

import pyBigWig
import numpy as np
import pandas as pd 
import math
import datetime
import sys

#--------------hyperparameter--------------------
basic_path = '/homes/jjyu/higlass_projects'
Input_bw_path = '%s/Input/DNase_bw_v1' %basic_path
Output_path = '%s/Output/' %basic_path
filter_data = pd.read_csv('%s/Input/04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv' % basic_path,sep=",")
seletedsample = pd.read_csv("%s/Input/seletedsample_recluster(222).txt" %basic_path, sep='\t',header=None, index_col=None)
allchrinfo = pd.read_csv("%s/Input/chromInfo.txt.allchr" %basic_path, sep='\t',header=None, index_col=None)
resolution = 1000
#------------------------------------------------

#all bw name list:
sample_list = seletedsample.iloc[:,0].tolist()
sample_ID = [sample.split(',')[3] for sample in sample_list]
bw_name = [sampleid + "_treat.bw" for sampleid in sample_ID]
#all chr name list:
allchrname_list = allchrinfo.iloc[0:24,0].tolist()

allchrname_length = allchrinfo.iloc[0:24,1].tolist()
#defind a normalization function
def normalization(x):
    Whole_mean = sum(x)/len(x)
    new_series = pd.Series(x)/Whole_mean
    new_list = new_series.tolist()
    return(new_list)

#test
bw_name = bw_name[0:222]
sample_list = sample_list[0:222]

print(int(sys.argv[1]))

allchrname_list = [[allchrname] for allchrname in allchrname_list] #this just for run chr one by one 
allchrname_list = allchrname_list[int(sys.argv[1])]
allchrname_length = [[i] for i in allchrname_length]
allchrname_length = allchrname_length[int(sys.argv[1])]

for a in range(len(allchrname_list)):
    starttime = datetime.datetime.now()
    chromo = allchrname_list[0]
    #Firsthalf
    length_chromo = allchrname_length[0]
    #Firsthalf_empty
    df_Firsthalf_empty = pd.DataFrame(columns=["chr_name", "start", "end"])
    df_Firsthalf_empty.chr_name = [chromo] * math.ceil(length_chromo/resolution)
    df_Firsthalf_empty.start = np.arange(0,length_chromo,resolution)
    df_Firsthalf_empty.end = np.append(np.arange(resolution,length_chromo,resolution),length_chromo)
    #lasthalf_empty
    df_lasthalf_empty = pd.DataFrame(columns = sample_list)
    for b in range(len(bw_name)):
        bw_file = bw_name[b]
        print("This is %s.th file:%s in %s" %(b+1,bw_file,chromo))
        #input_folder = 'dataset' + str(filter_data.DatsetId[i])
        input_file = '%s/%s' %(Input_bw_path, bw_file)
        try:
            bw = pyBigWig.open(input_file)
        except RuntimeError:
            print("This is a error file.")
            continue
        if (chromo in bw.chroms().keys()):
            chromo_values = bw.values(chromo,0,bw.chroms(chromo))
            chromo_values_array = np.array(chromo_values)
            chromo_values_array = np.nan_to_num(chromo_values_array)
            chromo_values = chromo_values_array.tolist()
            #print(chromo_values)
            chromo_values_split16 = [chromo_values[i:i + resolution] for i in range(0, len(chromo_values), resolution)]
            #chromo_values_split16_mean = [np.mean(x) for x in chromo_values_split16]
            def listmean(x):
                x_mean = np.mean(x)
                return(x_mean)
            chromo_values_split16_mean = list(map(listmean,chromo_values_split16))
            chromo_values_split16_mean_norm = normalization(chromo_values_split16_mean) #add speed
            #print(sum(chromo_values_split16_mean_norm))
            #print(chromo_values_split16_mean_norm[0:10])
            df_lasthalf_empty.iloc[:,b] = chromo_values_split16_mean_norm
            bw.close()
            print("\t")
        else:
            print("%s is not in the %s" %(chromo, bw))
            df_lasthalf_empty.iloc[:,b] = [0]*math.ceil(length_chromo/resolution)
            bw.close()
            print("\t")
            #concat two dataframe
    df_merge = pd.concat([df_Firsthalf_empty, df_lasthalf_empty], axis=1)
    print("This is the shape of %s matrix: %s" %(chromo,df_merge.shape))
    df_merge.to_csv('%s/bedfile_1000_222_%s.csv' %(Output_path,chromo), sep='\t',index=False, header=True)
    endtime = datetime.datetime.now()
    print (endtime - starttime)

