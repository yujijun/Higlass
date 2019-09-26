#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:41:09 2019

@author: yujijun
"""
import matplotlib.pyplot as plt 
import seaborn as sns

font={'family':'serif',
     'style':'italic',
    'weight':'normal',
      #'color':'black',
      'size':16
}

def cor_heatmap(matrix, Figsize, Figurename,out):
    """
    This script is for samples heatmap of correlation;
    Parameter: 
        matirx: rows:samples columns:feature
        Figsize: Tuple (It is the size of figure you like to output)
        Figurename: format:string; This is the plot name and figure title
    Returns:
        Samples correlation heatmap
    """
    plt.figure(figsize = Figsize)
    corr = matrix.T.corr()
    ax = sns.heatmap(
        corr, 
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True
    )
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right',
        fontdict=font
    );
       
    ax.set_yticklabels(
        ax.get_yticklabels(),
        fontdict = font
    );
    ax.set_title(Figurename,size=25)
    figure_name = '%s.png' %Figurename
    plt.tight_layout()
    plt.savefig('%s/%s' %(out,figure_name))