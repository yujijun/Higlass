#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:44:53 2019

@author: yujijun
"""
import matplotlib.pyplot as plt 
from scipy.cluster.hierarchy import dendrogram, linkage,fcluster

font={'family':'serif',
     'style':'italic',
    'weight':'normal',
      #'color':'black',
      'size':10,
      'fontweight':'bold'
}
def clusterplot(dist_mat, sample_list, sample_color_dict, Distance, Method, figurename, figuresize, out, havexlabel=True):
    """
    This acript is for hist plot
    
    parameter:
        dist_mat: format:dataframe rows:samples; columns: features.
        sample_list: format:list; this is the samples list.
        sample_color_dict: format:dict; {sample:sample_color}.
        Distance: format:string; this is calculation distance you would like to use,just like:correlation.
        Method: format:string; This is the cluster method you would like to use, just like:complete.
        figurename: format:string;This is the figure title and figure output name.
        out: format:string; This is the figure output path.
    
    Returns:
        Hist plot of all samples.
    """
    linkage_matrix = linkage(dist_mat, metric=Distance, method=Method)
    fig = plt.figure(figsize=figuresize)
    #Distance_Method = '_'.join([Distance,Method])
    dendrogram(linkage_matrix,labels=sample_list, leaf_font_size=12)
    ax = plt.gca()
    ax.set_title(figurename,size=30)
    xlbls = ax.get_xmajorticklabels()
    for lbl in xlbls:
        lbl.set_color(sample_color_dict[lbl.get_text()])
    if (havexlabel):
        ax.set_xticklabels(
            ax.get_xticklabels(),
            #rotation=45,
            horizontalalignment='right',
            fontdict=font
            )
    else:
        plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
    figure_name = '%s.png' %figurename
    plt.tight_layout()
    plt.savefig('%s/%s' %(out,figure_name))
    labels = [item.get_text() for item in ax.get_xticklabels()]
    return (labels)
