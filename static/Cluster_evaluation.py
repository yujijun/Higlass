#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 17:01:28 2019

@author: yujijun
"""
from sklearn import metrics
# Given Label:
def Clu_Eval_Givenlabels(labels_true, labels_pred):
    #The format should be list
    ARI = metrics.adjusted_rand_score(labels_true,labels_pred)
    AMI = metrics.adjusted_mutual_info_score(labels_true, labels_pred)
    return ARI,AMI

# Given Label:
def Clu_Eval_NotGivenlabels(x, labels,distance):
    """
    This script is to evaluate the cluster result.
    
    Parameters(DB):
    X : array-like, shape (n_samples, n_features)
List of n_features-dimensional data points. Each row corresponds to a single data point.
   labels : array-like, shape (n_samples,);Predicted labels for each sample.
   
   Returns(DB):
       score: format: float.
       The resulting Daview-Bouldin score.
       the minimum score is zero, with lower values indecating better clustering

    Parameters(Sil):
        X : array [n_samples_a, n_samples_a] if metric == “precomputed”, or, [n_samples_a, n_features] otherwise
Array of pairwise distances between samples, or a feature array.
        labels : array, shape = [n_samples],Predicted labels for each sample.
        metric : string, or callable
 The metric to use when calculating distance between instances in a feature 
 array. If metric is a string, it must be one of the options allowed by 
 metrics.pairwise.pairwise_distances. If X is the distance array itself, 
 use metric="precomputed".
     
     Returns(Sil):
         silhouette:float
         Mean Sihouette Coefficient for all samples.
    """
    DB = metrics.davies_bouldin_score(x,labels)
    Sil = metrics.silhouette_score(x,labels, distance)
    return DB,Sil


#Distances = ['euclidean', 'cosine', 'sqeuclidean', 'correlation', 'jaccard','canberra','braycurtis']
#Methods = ['single','complete','average','centroid','median','ward']
