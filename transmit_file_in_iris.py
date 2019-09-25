#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 17:19:28 2019
@author: yujijun
Description: This is a script for bw file transmit in iris server
（ssh -p 33001 jjyu@cistrome.org）
Input:04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv

"""

import pyBigWig
import pandas as pd 
from shutil import copyfile
basic_path = '/project/dev/jjyu/DNase_summary'
Input_path = '%s/Input' %basic_path
Output_path = '%s/DNase_bw_v1' %basic_path
filter_data = pd.read_csv('%s/04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv' % Input_path,sep="\t")


#filter_data.DatsetID = [1,6]
for i in range(len(filter_data)):
    print("This is %s .th file." %(i+1) )
    #input_folder = 'dataset' + str(filter_data.DatsetId[i])
    bigwig_path = filter_data.bigwig[i]
    print(bigwig_path)
    try:
        bw = pyBigWig.open(bigwig_path)
    except RuntimeError:
        print("This is a error file.")
        continue
    if ('chr22' in bw.chroms().keys()):
        copyfile(bigwig_path,Output_path)
        bw.close()
        print("\t")
        
