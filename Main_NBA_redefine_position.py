#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 13:57:10 2018

@author: jinzhao
"""

from Func_Web_Scrape_NBA import get_perGame_2018, get_perGame_header
from Func_redefine_pos import multiclass_visulization_PCA, multiclass_visulization_LDA, multiclass_visulization_Kmeans
import numpy as np
import csv
import matplotlib.pyplot as plt



if __name__ == '__main__':
    # Part A. Load data
    # ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== 
    X = []
    y = []
    player_names = []
    i = 0
    with open('data_2018.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if i == 0:
                i += 1
            else:
                data = []
                for i in range(2, 26):
                    data.append(float(line[i]))
                X.append(data)
                y.append(float(line[26])) 
                player_names.append(line[0])   
    X = np.array(X)
    y = np.array(y)
 
    # Part B. Machine Learning
    # ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== 
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import confusion_matrix
    n_samples, n_features = X.shape
    n_labels = 5

    # 1. Dimensionality Reduction
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
    from sklearn.preprocessing import StandardScaler
    X_norm = StandardScaler().fit_transform(X)

    # <1> PCA
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----  
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_norm)
    multiclass_visulization_PCA(X_pca, y)
    
    # <2> LDA
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    lda = LinearDiscriminantAnalysis(n_components=2)
    X_lda = lda.fit_transform(X, y)
    multiclass_visulization_LDA(X_lda, y, player_names)
    '''
    # 2. Classification
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
    # <1> Decision Tree
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
    from sklearn.tree import DecisionTreeClassifier
    # LDA
    X_train, X_test, y_train, y_test = train_test_split(X_lda, y, random_state = 0)

    clf_dtree = DecisionTreeClassifier(max_depth = 2).fit(X_train, y_train)
    pred_dtree = clf_dtree.predict(X_test)
    score_dtree_lda = clf_dtree.score(X=X_test, y=y_test)
    
    # PCA
    X_train, X_test, y_train, y_test = train_test_split(X_pca, y, random_state = 0)

    clf_dtree_pca = DecisionTreeClassifier(max_depth = 2).fit(X_train, y_train)
    pred_dtree = clf_dtree_pca.predict(X_test)
    score_dtree_pca = clf_dtree_pca.score(X=X_test, y=y_test)
    print("score_dtree: ", score_dtree_lda)

    # <2> SVM
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
    from sklearn.svm import SVC
    X_train, X_test, y_train, y_test = train_test_split(X_lda, y, random_state = 0)

    clf_svm_linear = SVC(kernel = 'linear', C = 1).fit(X_train, y_train)
    pred_svm = clf_svm_linear.predict(X_test)
     
    # model accuracy for X_test  
    score_svm_lda = clf_svm_linear.score(X_test, y_test)
    print("score_svm: ", score_svm_lda)
    
    # <3>. KNN
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
    from sklearn.neighbors import KNeighborsClassifier
    X_train, X_test, y_train, y_test = train_test_split(X_lda, y, random_state = 0)

    knn = KNeighborsClassifier(n_neighbors = 7).fit(X_train, y_train)
    # accuracy on X_test
    score_knn_lda = knn.score(X_test, y_test)
    print("score_knn: ", score_knn_lda)

    '''
    # 2. Clustering
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
    # K means
    from sklearn.cluster import KMeans
    n_clusters = 8
    kmeans = KMeans(n_clusters, random_state=0).fit(X_lda)
    y_labels = kmeans.labels_
    
    for i in range(n_clusters):
        X_tmp = X_lda[y_labels == i]
        player_indexes = [idx for idx, label in enumerate(y_labels) if label == i]
        plt.figure(figsize=(10, 10))
        plt.scatter(X_tmp[:, 0], X_tmp[:, 1], c = 'r', s = 20)
        # Annotate samples
        for idx in player_indexes[0:10]:
            name = player_names[idx]
            plt.annotate(name, (X_lda[idx, 0], X_lda[idx, 1]))
        plt.show()
    
    multiclass_visulization_Kmeans(X_lda, y_labels)


    

    
    
    
    
    