#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 17:53:40 2019

@author: yujijun
"""
import matplotlib
import random
# generate a color dict for each tissue
def colordict(sample_list, sample_len):
    """
    This is the script to create a sample:color dict.

    Parameter:
        sample_list: format:list; This is a list of all samples
        sample_len: format:,list; This is a list of length of each type of samples.
    
    Returns:
        format: dict; {sample:color}
    """
#    colors = []
#    for i in matplotlib.colors.cnames.keys():
#        colors.append(i)
#    random.seed(20)
#    colors_random = random.sample(colors,len(sample_len))
    colors_ban = ["#8B7E66","#27408B","#551A8B","#CD8500",'#000000',
                     '#2F4F4F','#483D8B',"#4682B4","#458B00","#698B22",
                     '#006400','#DAA520','#CD5C5C','#104E8B','#008B8B',
                     '#EE0000','#698B69','#90EE90','#8B0000','#8B008B',
                     '#00008B','#A9A9A9','#696969','#1C1C1C','#EED2EE',
                     '#5D478B','#9F79EE','#68228B','#8B2252','#FF3E96',
                     '#8B5F65','#EEA2AD','#CD0000','#FF6347','#FF7F00',
                     '#8B5742','#CD3333','#FF4040','#8B658B','#8B8B00',
                     '#FFFF00','#6E8B3D','#76EE00','#E0FFFF','#0000EE',
                     '#3A5FCD','#473C8B','#836FFF','#CDB7B5','#EECFA1']
    sample_colors = []
    for i in range(len(sample_len)):
        sample_colors.extend([colors_ban[i]]*sample_len[i])
    
    sample_color_dict = dict(zip(sample_list, sample_colors))
    return sample_color_dict