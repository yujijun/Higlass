#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 18:45:50 2019
@author: yujijun
Description: sample cluster
Input:
    QC_file_name = '/Users/yujijun/Documents/01-Work/02-HiglassProject/01-DataFilter/Output_data/04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv'
    Peak_matrix_name = '/Users/yujijun/hg-tmp/bedfile_peak_16.csv'
    seletedsample = '/Users/yujijun/Documents/01-Work/02-HiglassProject/01-DataFilter/Output_data/Seletedsample_bycluster.txt'
Output:
    clustername.png
"""

import sys
import pandas as pd 
import numpy as np
import math
import time 
from collections import Counter
import matplotlib.pyplot as plt 
import matplotlib
import random
import warnings
from scipy.cluster.hierarchy import dendrogram, linkage,fcluster
sys.path.append(r'/Users/yujijun/Documents/01-Work/02-HiglassProject/01-DataFilter/Script/static')
#sys.path.append(r'/homes/jjyu/higlass_projects/Script/static/') # set up the path of package by yourself 
import Normalization 
from collections import Counter
import Cluster
import ClusterPlot
import Cluster_evaluation
import ColorDict
import Cor_heatmap
import LinePlot
import Normalization
warnings.filterwarnings("ignore")

# Step one: Add column's name to peak matrix
#--------------------hyperparameter--------------------
#basic_path = '/homes/jjyu/higlass_projects'
#Input_path = '%s/Input' %basic_path
#Output_path = '%s/Output/1308_manysample' %basic_path
#QC_name = '%s/04-Homo_sapiens_ca_DNase_afterQC906_withoutNone_25.csv' %Input_path
##-------------------------------------------------------------------
#
#
##Input data 
#Peak_matrix = pd.read_csv('%s/bedfile_peak_16.csv' %Output_path, sep='\t')
#QC_file  = pd.read_csv(QC_name, sep=',')
QC_file_name = '/Users/yujijun/Documents/01-Work/02-HiglassProject/01-DataFilter/Output_data/04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv'
Peak_matrix_name = '/Users/yujijun/hg-tmp/bedfile_peak_16.csv'
seletedsample = '/Users/yujijun/Documents/01-Work/02-HiglassProject/01-DataFilter/Output_data/Seletedsample_bycluster.txt'

QC_file = pd.read_csv(QC_file_name, sep =',')
Peak_matrix = pd.read_csv(Peak_matrix_name, sep= "\t")
Seletedsample_dataframe = pd.read_csv(seletedsample, sep='\t',header=None,index_col=None)
Seletedsample_list = Seletedsample_dataframe.iloc[:,0].tolist()

#New columns of peak matrix with information of Tissue,cell type,cell line and Id:
sample_name = [','.join(QC_file.ix[i,['Tissue','Cell_type','Cell_line']]) for i in range(len(QC_file))]
sample_name_withID = [','.join((sample_name[i],str(QC_file.DatsetId[i]))) for i in range(len(QC_file))]
Peak_matrix.columns = ['chr', 'start', 'end'] + sample_name_withID
Peak_matrix_seletedsample = Peak_matrix[Seletedsample_list]

#Step two: give all samples corresponding colors, same tissue with same color 
# Tissue statistic
Tissue_name_all = [Seletedsample_list[i].split(',')[0] for i in range(len(Seletedsample_list))]
Tissue_status = dict(Counter(Tissue_name_all))
Tissue_status_new = {}
Fetal_value = []
for key,value in Tissue_status.items():
    print(key)
    if "Fetal" in key:
        Fetal_value.append(value)
    else:
        Tissue_status_new[key] = value
Tissue_status_new["Fetal"] = sum(Fetal_value)

#seleted sample name sort by the dict key
sample_index_resort = []
sample_len_list = []
for key,value in Tissue_status_new.items():
    tissue = key
    print(tissue)
    All_tissue_list = Seletedsample_list
    if "Fetal" == tissue:
        index = [i  for i in range(len(All_tissue_list)) if tissue in All_tissue_list[i]]
        sample_index_resort = sample_index_resort + index
    else:
        index = [i  for i in range(len(All_tissue_list)) if All_tissue_list[i].split(',')[0] == tissue]
        sample_index_resort = sample_index_resort + index
    sample_len_list.append(value)  
Seletedsample_list_resort = [Seletedsample_list[i] for i in sample_index_resort]


#generate sample color dict 
sample_color_dict = ColorDict.colordict(Seletedsample_list_resort, sample_len_list)


#Cluster
dist_mat = Peak_matrix_seletedsample.T
dist_mat = dist_mat.fillna(0)
Distance = 'correlation'
Method = 'complete'
figurename = '222_correlation_complete'
figuresize = (60,10)
out = '/Users/yujijun/Desktop/'
#create diagram of cluster with the method of average:
Cluster_lables_average_cor_222 = ClusterPlot.clusterplot(dist_mat, Seletedsample_list, sample_color_dict, Distance, Method, figurename, figuresize, out, havexlabel=True)
with open('/Users/yujijun/Desktop/seletedsample_recluster.txt', 'w') as f:
    for item in Cluster_lables_average_cor_222:
        f.write("%s\n" %item)



