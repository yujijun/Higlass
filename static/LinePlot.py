#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 18:21:32 2019
This script is to generate a line chart for a DataFrame
@author: yujijun
"""
import numpy as np
import matplotlib.pyplot as plt
#import string 
#import matplotlib


def lineplot(dataframe,figurename,out, color, Figsize =(15,10), Hspace=0.2):
    """
    dataframe:
        format: DataFrame
        rows:samples 
        columns:feature
    Figsize:
        format:tuple default:(10,5)
    Hspace:
        format:integer default:0.2
        This is the distance between figure 
    figurename:
        format:string
        This is the figure title and plot name
    Retures:
        
    """
    columns_num = dataframe.shape[1]
    sample_list = dataframe.index.tolist()
    fig,axs = plt.subplots(columns_num, 1, figsize=Figsize, sharex=True)
    fig.subplots_adjust(hspace=0.5)
    #x = list(range(len(dataframe)))
    for i in range(columns_num):
        axs[i].plot(sample_list,dataframe.iloc[:,i], c=color)
        axs[i].set_title(dataframe.columns[i])
    plt.setp(axs[i].get_xticklabels(), rotation=30, ha="right",fontweight='bold',fontsize=10)
    #plt.title('%s' %figurename)
    figure_name = '%s.png' %figurename
    plt.tight_layout()
    plt.savefig('%s/%s' %(out,figure_name))
#lineplot(dist_mat_test,(15,8),Hspace=0.1)

#axs[i].xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
#axs[i].set_xticklabels(sample_list)

#str_list = list(string.ascii_letters)[0:10]
#dist_mat_test = sample_info_new.iloc[0:10,8:15] 
#dist_mat_test.index = str_list