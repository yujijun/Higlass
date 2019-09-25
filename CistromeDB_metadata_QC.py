#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:46:47 2019
@author: yujijun
Description: This is a script for CistromeDB metadata statistic and analysis:
we use the six index from http://cistrome.org/db/#/about to do filter.
Input: 
DC_haveProcessed_20190506_filepath.xls_compiled_database.xls
and DC_haveProcessed_20190506_filepath.xls

Output: 
01-Homo_sapiens_ca_DNase.csv 
02-Homo_sapiens_ca_DNase_QC(906).txt
"""
import pandas as pd 
import numpy as np
import warnings
from collections import Counter
warnings.filterwarnings('ignore')

Cutoff_FastQC = 25
Cutoff_UniquelyMappedRatio = 0.6
Cutoff_PBC = 0.8
Cutoff_FRiP = 0.01
Cutoff_MergedPeaksUnionDHSRatio = 0.7
Cutoff_PeaksFoldChange10 = 500

Input_path = '/Users/yujijun/Documents/01-Work/02-HiglassProject/01-DataFilter/Original_data/'
metadata_name = '%s/DC_haveProcessed_20190506_filepath.xls' %Input_path
QC_name = '%s/DC_haveProcessed_20190506_filepath.xls_compiled_database.xls' %Input_path
Output_path = '/Users/yujijun/Documents/01-Work/02-HiglassProject/01-DataFilter/Output_data/'

#######step one: data selected #########
#Data import 
metadata = pd.read_csv(metadata_name, sep="\t")
QCdata = pd.read_csv(QC_name,sep="\t")

#merge the data（This is the all data）
data_merge = pd.merge(metadata, QCdata, on="DatsetId")

#all homo sapiens data
data_merge_Homo_sapiens = data_merge[(data_merge.Species == "Homo sapiens")]

#all chromosome accessiblility data in homo sapiens
data_merge_Homo_sapiens_ca = data_merge_Homo_sapiens[(data_merge_Homo_sapiens.Factor_type == "ca")]
len(data_merge_Homo_sapiens[(data_merge_Homo_sapiens.Factor == "ATAC-seq")])
len(data_merge_Homo_sapiens[(data_merge_Homo_sapiens.Factor == "DNase")])

#output of the DNase in ca 
data_merge_Homo_sapiens_ca_DNase = data_merge_Homo_sapiens_ca[(data_merge_Homo_sapiens_ca.Factor == "DNase")]
data_merge_Homo_sapiens_ca_DNase.to_csv('%s/01-Homo_sapiens_ca_DNase.csv' %Output_path, index=False)


#############Step two:QC#################
data_merge_Homo_sapiens_ca_DNase_afterQC = data_merge_Homo_sapiens_ca_DNase[(data_merge_Homo_sapiens_ca_DNase["FastQC"] >= Cutoff_FastQC) 
                                                  & (data_merge_Homo_sapiens_ca_DNase["UniquelyMappedRatio"]>=Cutoff_UniquelyMappedRatio)
                                                  & (data_merge_Homo_sapiens_ca_DNase["PBC"]>=Cutoff_PBC) 
                                                  & (data_merge_Homo_sapiens_ca_DNase["FRiP"]>=Cutoff_FRiP)
                                                  & (data_merge_Homo_sapiens_ca_DNase["MergedPeaksUnionDHSRatio"]>=Cutoff_MergedPeaksUnionDHSRatio) 
                                                  & (data_merge_Homo_sapiens_ca_DNase["PeaksFoldChange10"] >=Cutoff_PeaksFoldChange10)]

data_merge_Homo_sapiens_ca_DNase_afterQC.to_csv('%s/02-Homo_sapiens_ca_DNase_QC(906).txt' %Output_path, index=False)

