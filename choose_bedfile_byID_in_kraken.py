#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:56:55 2019

@author: yujijun
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 11:17:29 2019
Description: This is a scripts to choose,cluster,sorted file in kraken 
@author: yujijun
Input: 
    04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv
    bedfile_16_543.csv
    cluster_DatsetId_439.txt
Output:
    bedfile_16_439_sorted.csv
    
    
"""
import pandas as pd 
#open the bed_16_v1 and replace the column names with DatsetId
basic = '/homes/jjyu/higlass_projects'
Input = '%s/Input' %basic
Output = '%s/Output' %basic
QC_file = pd.read_csv('%s/04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv %Input, sep=',')
DatsetId_all = QC_file.DatsetId.tolist()
bedfile = pd.read_csv('%s/higlass_543_16/bedfile_16_543.csv' %Output, sep='\t', header=None)
bedfile.columns = ['chr','start','end'] + DatsetId_all
print(bedfile.shape)

# choose the sorted ID with or without cluster
DatsetId_cluster = pd.read_csv('%s/cluster_DatsetId_439.txt' %Input,header=None)
DatsetId_cluster = DatsetId_cluster[0].tolist()
bedfile_v1 = bedfile.loc[:,['chr','start','end']+DatsetId_cluster]

#Output
bedfile_v1.to_csv('%s/1308_manysample/bedfile_16_439_sorted.csv' %Output, sep='\t',header=None)

