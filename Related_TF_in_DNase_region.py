#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 13:19:04 2019

@author: yujijun
"""
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import pyBigWig
import collections
import scipy.stats as ss
# input index and sample name information 
basic_path = "/Users/yujijun/Documents/01-Work/02-HiglassProject/03-interpret/Output/index_info" # 
index_name = "Blood_index.txt"
info_name = "Blood_info.txt"

blood_index = pd.read_csv("%s/%s" %(basic_path,index_name),sep='\t',header=None,index_col=None)
blood_info = pd.read_csv("%s/%s" %(basic_path,info_name),sep='\t',header=None,index_col=None)

data = {"index":blood_index.iloc[:,0],"info":blood_info.iloc[:,0]}
df = pd.DataFrame(data)
choose_sample_20 = df.iloc[20,:]

#input blood92 chromosome and choose special sample 
blood92_path = "/Users/yujijun/Documents/01-Work/02-HiglassProject/03-interpret/Output/bedfile_1000_blood92"
blood92_chr1_name = "bedfile_1000_Blood92_chr1.csv"
input_blood92 = pd.read_csv("%s/%s" %(blood92_path,blood92_chr1_name),sep='\t',header=0,index_col=None)
start_index = input_blood92[input_blood92.start==62780000].index.values[0]
end_index = input_blood92[input_blood92.start==62820000].index.values[0]

choose_data = input_blood92.iloc[list(range(start_index,end_index)),27]
fig, ax = plt.subplots(figsize=(15,5))
x = np.arange(start_index*1000, (end_index)*1000,1000)
plt.plot(x,choose_data,color="#FF8C00")
plt.xticks(rotation=90)
#ax.xaxis.set_major_locator(MultipleLocator(1))
#


#handle the TF data 
input_path = "/Users/yujijun/Documents/01-Work/02-HiglassProject/03-interpret/Input_file/DNase_bw_v2"
sample_ID_list = [35477,36245,42217,43825,4550,46156,53417]
correlation_list = []
for i in sample_ID_list:
    bigwig_file = "%s/%s_treat.bw" %(input_path,str(i))
    print(bigwig_file)
    bw = pyBigWig.open(bigwig_file)
    resolution = 1000
    chromo = "chr1"
    chromo_values = bw.values(chromo,0,bw.chroms(chromo))
    chromo_values_split1000 = [chromo_values[i:i + resolution] for i in range(start_index*1000, end_index*1000, resolution)]
    def listmean(x):
        x_mean = np.mean(x)
        return(x_mean)
    chromo_values_split1000_mean = list(map(listmean,chromo_values_split1000))
    
    whole_mean = np.nansum(chromo_values)/len(chromo_values)
    new_series = pd.Series(chromo_values_split1000_mean)/whole_mean
    new_list = new_series.tolist()
    #print(chromo_values_split16_mean[0:10])
    chromo_values_split1000_mean_norm = new_list #add speed
    correlation = np.corrcoef(choose_data,chromo_values_split1000_mean_norm)
    correlation_list.append(correlation[1,0])
    bw.close()

data = {"sample_ID":sample_ID_list, "correlation":correlation_list}
df_correlation = pd.DataFrame(data,index=range(len(sample_ID_list)))
df_correlation.sort_values("correlation",inplace=True,ascending=False)


#input summmit file 
sample_ID_list = [35477,36245,42217,43825,4550,46156,53417]
correlation_list = []
for i in sample_ID_list:
    summit_file = "%s/%s_sort_summits.bed" %(input_path,str(i))
    summit = pd.read_csv(summit_file,header=None, sep='\t')
    summit_chr1 = summit[summit.iloc[:,0] == "chr1"]
    summit_chr1 = summit_chr1[(start_index*1000) <= summit_chr1.iloc[:,1]]
    summit_chr1 = summit_chr1[summit_chr1.iloc[:,1] <= (end_index*1000)]
    
    peak_list = summit_chr1.iloc[:,1].tolist()
    x = np.arange(start_index*1000, (end_index)*1000,1000)
    
    peak_data = [0]*len(x)
    for i in peak_list:
        for j in range(len(x)-1):
            if i>=x[j] and i<x[j+1]:
                index_i = summit_chr1[summit_chr1.iloc[:,1] == i].index.values[0]
                peak_data[j] = summit_chr1.ix[index_i,4]
    correlation = np.corrcoef(choose_data,peak_data)
    correlation_list.append(correlation[1,0])
data = {"sample_ID":sample_ID_list, "correlation":correlation_list}
df_correlation = pd.DataFrame(data,index=range(len(sample_ID_list)))
df_correlation.sort_values("correlation",inplace=True,ascending=False)


#define some of the function:
def summit_allmean(sample_ID_list):
    summit_allmean_list = []
    for i in sample_ID_list:
        summit_file = "%s/%s_sort_summits.bed" %(input_path,str(i))
        summit = pd.read_csv(summit_file,header=None, sep='\t')
        summit_allsum = np.nansum(summit.iloc[:,4])
        summit_allmean_list.append(summit_allsum/len(summit))
    return(summit_allmean_list)
summit_allmean_list = summit_allmean(sample_ID_list)

#meannormalize
def meannormalize(df_input,summit_allmean_list):
    for i in range(len(df_input)):
        df_input.iloc[i,:] = df_input.iloc[i,:].values/summit_allmean_list[i]
    return(df_input)
    
#quantileNormalize 
def quantileNormalize(df_input):
    df = df_input.copy()
    #compute rank
    dic = {}
    for col in df:
        dic.update({col : sorted(df[col])})
    sorted_df = pd.DataFrame(dic)
    rank = sorted_df.mean(axis = 1).tolist()
    #sort
    for col in df:
        t = np.searchsorted(np.sort(df[col]), df[col])
        df[col] = [rank[i] for i in t]
    return df
#ranknormalize
def ranknormalize(df_input):
    for i in range(df_input.shape[1]):
        columns_rank = ss.rankdata(df_input.iloc[:,i].values)
        df_input.iloc[:,i] = columns_rank
    return(df_input)
    
#find the peaks in a specific region 
region_list_all =[[62800000,62802000],[62796000,62797000]]
sample_ID_list = [35477,36245,42217,43825,4550,46156,53417]
def find_peak_singleregion(input_path,sample_ID_list,region_list_single):
    start = region_list_single[0]
    end = region_list_single[1]
    peak_value_list = []
    for i in sample_ID_list:
        summit_file = "%s/%s_sort_summits.bed" %(input_path,str(i))
        summit = pd.read_csv(summit_file,header=None, sep='\t')
        summit_chr1 = summit[summit.iloc[:,0] == "chr1"]
        summit_chr1 = summit_chr1[start <= summit_chr1.iloc[:,1]]
        summit_chr1 = summit_chr1[summit_chr1.iloc[:,1] <= end]
        
        #if there is a data in summit_chr1 
        if len(summit_chr1) == 0:
            peak_value_list.append(0)
        elif len(summit_chr1) == 1:
            peak_value_list.append(summit_chr1.iloc[:,4].values[0])
        else:
            peak_value_list.append(np.nanmean(summit_chr1.iloc[:,4].values))
    return(peak_value_list)

def find_peak_singleregion_nonpeakvalue(input_path,sample_ID_list,region_list_single):
    start = region_list_single[0]
    end = region_list_single[1]
    peak_value_list = []
    for i in sample_ID_list:
        summit_file = "%s/%s_sort_summits.bed" %(input_path,str(i))
        summit = pd.read_csv(summit_file,header=None, sep='\t')
        summit_chr1 = summit[summit.iloc[:,0] == "chr1"]
        summit_chr1 = summit_chr1[start <= summit_chr1.iloc[:,1]]
        summit_chr1 = summit_chr1[summit_chr1.iloc[:,1] <= end]
        
        #if there is a data in summit_chr1 
        if len(summit_chr1) == 0:
            peak_value_list.append(0)
        elif len(summit_chr1) == 1:
            peak_value_list.append(1)
        else:
            peak_value_list.append(1)
    return(peak_value_list)

def find_peak_allregion(input_path,sample_ID_list,region_list_all):
    peak_list_all = []
    for i in range(len(region_list_all)):
        peak_list = find_peak_singleregion(input_path,sample_ID_list,region_list_all[i])
        peak_list_all.append(peak_list)
    #print(peak_list_all)
    colume_names = ["region"+str(i) for i in range(1,len(region_list_all)+1)]   
    dict_peak = dict(zip(colume_names,peak_list_all))
    df = pd.DataFrame(dict_peak)
    df.index = sample_ID_list
    return(df)

def find_peak_allregion_nonpeakvalue(input_path,sample_ID_list,region_list_all):
    peak_list_all = []
    for i in range(len(region_list_all)):
        peak_list = find_peak_singleregion_nonpeakvalue(input_path,sample_ID_list,region_list_all[i])
        peak_list_all.append(peak_list)
    #print(peak_list_all)
    colume_names = ["region"+str(i) for i in range(1,len(region_list_all)+1)]   
    dict_peak = dict(zip(colume_names,peak_list_all))
    df = pd.DataFrame(dict_peak)
    df.index = sample_ID_list
    return(df)

def weighted_sum(df_qn):
    weight = 1/df_qn.shape[1]
    weighted_sum_list = []
    for i in range(df_qn.shape[0]):
        weighted_sum = np.sum(df_qn.iloc[i,:].values*weight)
        weighted_sum_list.append(weighted_sum)
    columnname_list = [str(i) for i in df_qn.index.tolist()]
    dict_weighted_sum = {"sample_ID":columnname_list, "weighted_sum":weighted_sum_list}
    df = pd.DataFrame(dict_weighted_sum)
    df_sort = df.sort_values(by=["weighted_sum"],ascending=False)
    return(df_sort)

#original peak dataframe + quantileNormalize
df = find_peak_allregion(input_path=input_path,sample_ID_list=sample_ID_list,region_list_all=region_list_all)
df_qn = quantileNormalize(df)
df_qn_weighted_sum = weighted_sum(df_qn)  


#meannormalization dataframe + quantileNormalize
df = find_peak_allregion(input_path=input_path,sample_ID_list=sample_ID_list,region_list_all=region_list_all)
df_meannorm = meannormalize(df,summit_allmean_list)
df_mean_qn = quantileNormalize(df_meannorm)
df_mean_qn_weighted_sum = weighted_sum(df_mean_qn)   

#meannormlization dataframe + ranknormalization 
df = find_peak_allregion(input_path=input_path,sample_ID_list=sample_ID_list,region_list_all=region_list_all)
df_meannorm = meannormalize(df,summit_allmean_list) 
df_mean_rank = ranknormalize(df_meannorm)  
df_mean_ranknorm_weighted_sum = weighted_sum(df_mean_rank)

#meannormlization + nonpeaknumber + weighted sum
df_nonpeakvalue = find_peak_allregion_nonpeakvalue(input_path=input_path,sample_ID_list=sample_ID_list,region_list_all=region_list_all)
df_nonpeakvalue_weighted_sum = weighted_sum(df_nonpeakvalue)
