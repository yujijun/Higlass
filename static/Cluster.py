#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 13:54:38 2019

@author: yujijun
"""
from scipy.cluster.hierarchy import dendrogram, linkage,fcluster

def cluster(dist_mat, Distance, Method, n_cluster):
    """
    This script is to generate a cluster result by scipy.cluster.hierarchy
    
    Parameter:
        dist_mat: format:DataFrame; rows:samples; columns:features
        Distance: format:string; The distance method you would like to use,just like "correlation".
        Method: format:string; The cluster method you would like to use,just like "complete".
        n_cluster: format:integer; This is the number of cluster.
        
    Returns:
        format:list; The is the cluster result of all sample.
    """
    linkage_matrix = linkage(dist_mat, metric=Distance, method=Method)
    clust_pred = fcluster(linkage_matrix, t=n_cluster,criterion="maxclust")
    return clust_pred

