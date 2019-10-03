#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 18:39:09 2019
Description:This scripts is for the statistic and choose sample and disease information
@author: yujijun
"""
import pandas as pd 
import numpy as np
from collections import Counter 
Input_path = '/Users/yujijun/Documents/01-Work/02-HiglassProject/01-DataFilter/Output_data'
DNase_name = "%s/01-Homo_sapiens_ca_DNase.csv" %Input_path
DNase_name_qc = "%s/03-Homo_sapiens_ca_DNase_QC(906)_add_info_manually.csv" %Input_path
DNase = pd.read_csv(DNase_name, sep=',',header=0,index_col=0)
DNase_qc = pd.read_csv(DNase_name_qc, sep=',',header=0,index_col=0)

tissue = dict(Counter(DNase_qc.Tissue))
key_tissue_disease = []
key_tissue_disease_value = []
for key_tissue,value in tissue.items():
    if "None" not in key_tissue and "Fetal" not in key_tissue:
        Disease_index = DNase_qc[DNase_qc['Tissue'].isin([key_tissue])].index
        Disease = DNase.loc[Disease_index.tolist(),'Disease']
        disea_dict = dict(Counter(Disease))
        for key_disease,value_disease in disea_dict.items():
            key_tissue_disease.append("_".join([key_tissue,key_disease]))
            key_tissue_disease_value.append(value_disease)
            
        
df =  pd.DataFrame(list(zip(key_tissue_disease,key_tissue_disease_value)),columns=["Tissue_disease","Value"])           

df.to_csv("%s/tissue_disease_statistic_qc.txt"%Input_path,sep='\t',header=True,index=None)


#choose the tissue and seleted sample ID 
### Lung ####
Lung = DNase_qc[DNase_qc['Tissue'].isin(["Lung"])]
Lung_Normal_index = Lung[Lung['Disease'].isin(["Normal"])].index
Lung_cancer_index = Lung[Lung['Disease'].isin(["Lung Carcinoma"])].index

Lung_index = Lung_Normal_index.tolist() + Lung_cancer_index.tolist()

with open('%s/Lung_index.txt' %Input_path, 'w') as f:
    for item in Lung_index:
        f.write("%s\n" %item)
        
Lung_info_list = []
for index in Lung_index:
    Lung_info = DNase_qc.loc[index,["Cell_line","Cell_type","Tissue","Disease"]].tolist()
    Lung_info_list.append(",".join(Lung_info))   
with open('%s/Lung_info.txt' %Input_path, 'w') as f:
    for item in Lung_info_list:
        f.write("%s\n" %item)

###tissue####
Blood = DNase_qc[DNase_qc['Tissue'].isin(["Blood"])]
Blood_all = Blood.index
Blood_Normal_index = Blood[Blood['Disease'].isin(["Normal"])].index
Blood_None = Blood[Blood['Disease'].isin(["None"])].index
Blood_cancer_normal = Blood_all.difference(Blood_None)
Blood_cancer = Blood_cancer_normal.difference(Blood_Normal_index)
Blood_index = Blood_Normal_index.tolist() + Blood_cancer.tolist()

with open('%s/Blood_index.txt' %Input_path, 'w') as f:
    for item in Blood_index:
        f.write("%s\n" %item)
        
Blood_info_list = []
for index in Blood_index:
    Blood_info = DNase_qc.loc[index,["Cell_line","Cell_type","Tissue","Disease"]].tolist()
    Blood_info_list.append(",".join(Blood_info))   
with open('%s/Blood_info.txt' %Input_path, 'w') as f:
    for item in Blood_info_list:
        f.write("%s\n" %item)

###kidney###
Kidney = DNase_qc[DNase_qc['Tissue'].isin(["Kidney"])]
Kidney_Normal_index = Kidney[Kidney['Disease'].isin(["Normal"])].index
Kidney_cancer_index = Kidney[Kidney['Disease'].isin(["Carcinoma"])].index

Kidney_index = Kidney_Normal_index.tolist() + Kidney_cancer_index.tolist()

with open('%s/Kidney_index.txt' %Input_path, 'w') as f:
    for item in Kidney_index:
        f.write("%s\n" %item)
        
Kidney_info_list = []
for index in Kidney_index:
    Kidney_info = DNase_qc.loc[index,["Cell_line","Cell_type","Tissue","Disease"]].tolist()
    Kidney_info_list.append(",".join(Kidney_info))   
with open('%s/Kidney_info.txt' %Input_path, 'w') as f:
    for item in Kidney_info_list:
        f.write("%s\n" %item)

def tiss_disea(list1):
    #['Tissue','Normal','Carcinoma']
    tissue = DNase_qc[DNase_qc['Tissue'].isin([list1[0]])]
    tissue_Normal_index = tissue[tissue['Disease'].isin([list1[1]])].index
    tissue_cancer_index = tissue[tissue['Disease'].isin([list1[2]])].index
    
    tissue_index = tissue_Normal_index.tolist() + tissue_cancer_index.tolist()
    
    with open('%s/%s_index.txt' %(Input_path,list1[0]), 'w') as f:
        for item in tissue_index:
            f.write("%s\n" %item)
    print(len(tissue_index))
    tissue_info_list = []
    for index in tissue_index:
        tissue_info = DNase_qc.loc[index,["Cell_line","Cell_type","Tissue","Disease"]].tolist()
        tissue_info_list.append(",".join(tissue_info))   
    with open('%s/%s_info.txt' %(Input_path,list1[0]), 'w') as f:
        for item in tissue_info_list:
            f.write("%s\n" %item)
tiss_disea(['Skin','Normal','Melanoma'])
tiss_disea(['Prostate','Normal','Prostate Carcinoma'])
tiss_disea(['Breast','Breast cancer','Ductal Carcinoma'])
tiss_disea(['Eye','Normal','Retinoblastoma'])
tiss_disea(['Thymus','Normal','Papillary thyroid carcinoma'])
tiss_disea(['Colon','Colorectal Adenocarcinoma','Colorectal cancer'])
###def all kinds disease in tissue####
def tiss_disea_kinds(string):
    #string of tissue
    tissue = DNase_qc[DNase_qc['Tissue'].isin([string])]
    tissue_all = tissue.index
    tissue_Normal_index = tissue[tissue['Disease'].isin(["Normal"])].index
    tissue_None = tissue[tissue['Disease'].isin(["None"])].index
    tissue_cancer_normal = tissue_all.difference(tissue_None)
    tissue_cancer = tissue_cancer_normal.difference(tissue_Normal_index)
    tissue_index = tissue_Normal_index.tolist() + tissue_cancer.tolist()
    
    with open('%s/%s_index.txt' %(Input_path,string), 'w') as f:
        for item in tissue_index:
            f.write("%s\n" %item)
    print(len(tissue_index))    
    tissue_info_list = []
    for index in tissue_index:
        tissue_info = DNase_qc.loc[index,["Cell_line","Cell_type","Tissue","Disease"]].tolist()
        tissue_info_list.append(",".join(tissue_info))   
    with open('%s/%s_info.txt' %(Input_path,string), 'w') as f:
        for item in tissue_info_list:
            f.write("%s\n" %item)

tiss_disea_kinds('Brain')
tiss_disea_kinds('Bone Marrow')
tiss_disea_kinds('Embryo')

#Breast#
list1 = ['Breast','Breast cancer','Ductal Carcinoma']
Breast = DNase_qc[DNase_qc['Tissue'].isin([list1[0]])]
Breast_cancer_index = Breast[Breast['Disease'].isin([list1[1]])].index
Breast_Ductal_carcinoma_index = Breast[Breast['Disease'].isin([list1[2]])].index

Mammary_Gland = DNase_qc[DNase_qc['Tissue'].isin(["Mammary Gland"])]
Mammary_Gland_Normal_index = Mammary_Gland[Mammary_Gland['Disease'].isin(["Normal"])].index
Mammary_Gland_cancer_index = Mammary_Gland[Mammary_Gland['Disease'].isin(["Breast cancer"])].index
Breast_index = Breast_cancer_index.tolist() + Mammary_Gland_cancer_index.tolist() + Breast_Ductal_carcinoma_index.tolist() + Mammary_Gland_Normal_index.tolist()

with open('%s/%s_index.txt' %(Input_path,"Breast"), 'w') as f:
    for item in Breast_index:
        f.write("%s\n" %item)
print(len(Breast_index))    
Breast_info_list = []
for index in Breast_index:
    Breast_info = DNase_qc.loc[index,["Cell_line","Cell_type","Tissue","Disease"]].tolist()
    Breast_info_list.append(",".join(Breast_info))   
with open('%s/%s_info.txt' %(Input_path,"Breast"), 'w') as f:
    for item in Breast_info_list:
        f.write("%s\n" %item)
        
#Lung_index = pd.read_csv('%s/Lung_index.txt' %Input_path, sep='\t',header=None, index_col=None)
#Lung_info = pd.read_csv('%s/Lung_info.txt' %Input_path, sep='\t',header=None, index_col=None)
#sample_list = Lung_info.iloc[:,0].tolist()
#Lung_index_list = Lung_index.iloc[:,0].tolist()
#bw_name = [str(sampleid) + "_treat.bw" for sampleid in Lung_index_list]
