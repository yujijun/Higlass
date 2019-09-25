#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:56:15 2019
@author: yujijun
Description:
    QC by FRiP >= 0.25 and filter out non-information tissues 

Input: 
    03-Homo_sapiens_ca_DNase_QC(906)_add_info_mannually.csv
Output:
    04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv
    
"""
import pandas as pd 
import numpy as np
import warnings
from collections import Counter
warnings.filterwarnings('ignore')

Input_path = '/Users/yujijun/Documents/01-Work/02-HiglassProject/01-DataFilter/Original_data/'
Output_path = '/Users/yujijun/Documents/01-Work/02-HiglassProject/01-DataFilter/Output_data/'

Cutoff_FastQC = 25
Cutoff_UniquelyMappedRatio = 0.6
Cutoff_PBC = 0.8
Cutoff_FRiP = 0.01
Cutoff_MergedPeaksUnionDHSRatio = 0.7
Cutoff_PeaksFoldChange10 = 500


#step one: QC 
Ca_DNase_QC906 = pd.read_csv('%s/03-Homo_sapiens_ca_DNase_QC(906)_add_info_manually.csv' %Output_path, sep=',')
Ca_DNase_QC906_withoutNone = Ca_DNase_QC906[Ca_DNase_QC906.Tissue != 'None']
Ca_DNase_QC906_withoutNone_25 = Ca_DNase_QC906_withoutNone[(Ca_DNase_QC906_withoutNone["FastQC"] >= Cutoff_FastQC) 
                                                  & (Ca_DNase_QC906_withoutNone["UniquelyMappedRatio"]>=Cutoff_UniquelyMappedRatio)
                                                  & (Ca_DNase_QC906_withoutNone["PBC"]>=Cutoff_PBC) 
                                                  & (Ca_DNase_QC906_withoutNone["FRiP"]>=0.25)
                                                  & (Ca_DNase_QC906_withoutNone["MergedPeaksUnionDHSRatio"]>=Cutoff_MergedPeaksUnionDHSRatio) 
                                                  & (Ca_DNase_QC906_withoutNone["PeaksFoldChange10"] >=Cutoff_PeaksFoldChange10)]
Ca_DNase_QC906_withoutNone_25.to_csv('%s/04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv' %Output_path, index=False)




# step two:Statistic 
Tissue_status = Counter(Ca_DNase_QC906_withoutNone_25.Tissue)
Tissue_status.most_common()

#or 
Tissue_status = dict(Counter(Ca_DNase_QC906_withoutNone_25.Tissue))
sorted_tissue_status = sorted(Tissue_status.items(), key= lambda kv:kv[1], reverse=True)

#visualization
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(20,5))
x = np.arange(len(sorted_tissue_status))
x_name = [i[0] for i in sorted_tissue_status]
y = [i[1] for i in sorted_tissue_status]
plt.xticks(x,x_name)
plt.setp(ax.xaxis.get_majorticklabels(),rotation=90,fontweight='bold',color='#000000')
plt.bar(x,y,color='#CDBA96')
for i in x:
    plt.text(x=i-0.5, y=y[i]+1,s=y[i])