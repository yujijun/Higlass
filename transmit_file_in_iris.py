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
import os
import glob
basic_path = '/project/dev/jjyu/DNase_summary'
Input_path = '%s/Input' %basic_path
filter_data = pd.read_csv('%s/02-Homo_sapiens_ca_DNase_QC_906.txt' %Input_path,sep=",")

#filter_data = pd.read_csv('/Users/yujijun/Documents/01-Work/02-HiglassProject/01-DataFilter/Output_data/04-Homo_sapiens_ca_DNase_QC(906)_non-info-tissue_FRiP0p25(543).csv', sep=',')
#if True:
#    #transmit the file correct and with chr22 information
#    for i in range(len(filter_data)):
#        Output_path = '%s/DNase_bw_v1/' %basic_path
#        print("This is %s .th file." %(i+1) )
#        bigwig_path = filter_data.bigwig[i]
#        print(bigwig_path)
#        try:
#            bw = pyBigWig.open(bigwig_path)
#        except RuntimeError:
#            print("This is a error file.")
#            continue
#        if ('chr22' in bw.chroms().keys()):
#            filepath,filename = os.path.split(bigwig_path)
#            Output_path = Output_path + filename
#            copyfile(bigwig_path,Output_path)
#            bw.close()
#            print("\t")
#else:
    #transmit the file correct and with correct file and any of chr information
bw_error_list = [] 
for i in range(len(filter_data)):
    Output_path = '%s/DNase_bw_v1/' %basic_path
    print("This is %s .th file." %(i+1) )
    #input_folder = 'dataset' + str(filter_data.DatsetId[i])
    bigwig_path = filter_data.bigwig[i]
    filepath,filename = os.path.split(bigwig_path)
    all_ex_filelist = glob.glob('%s/DNase_bw_v1/*.bw' %basic_path)
    all_ex_filenamelist = [os.path.split(i)[1] for i in all_ex_filelist]
    if filename in all_ex_filenamelist:
        print("You already have this file.")
        continue
    try:
        bw = pyBigWig.open(bigwig_path)
    except RuntimeError:
        print("This is a error file.")
        continue
    Output_path = Output_path + filename
    copyfile(bigwig_path,Output_path)  
    bw.close()
    print("\t")

with open("%s/bw_error.txt" %basic_path) as f:
    for item in bw_error_list:
        f.write("%s\n" % item)
        
#bw_error_list = []   
#for i in range(len(filter_data)):
#    bigwig_path= '%s/DNase_bw_v1/' %basic_path
#    print("This is %s .th file." %(i+1))
#    summit_path_ori = filter_data.bigwig[i]
#    filepath,filename = os.path.split(summit_path_ori)
#    
#    all_ex_filelist = glob.glob('%s/DNase_bw_v1/*.bw' %basic_path)
#    all_ex_filenamelist = [os.path.split(i)[1] for i in all_ex_filelist]
#    if filename in all_ex_filenamelist:
#        print("You already have this file.")
#        continue
#    try:
#        bw = pyBigWig.open(summit_path_ori)
#    except RuntimeError:
#        print("This is a error file.")
#        bw_error_list.append(filename)
#        continue
#    submit_path = submit_path + filename
#    copyfile(summit_path_ori,submit_path)
#    bw.close()
#    print("\t")
#
#with open("%s/bw_error.txt" %basic_path) as f:
#    for item in bw_error_list:
#        f.write("%s\n" % item)
        
