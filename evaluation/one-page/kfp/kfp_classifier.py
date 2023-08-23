#!/usr/bin/env python3

"""
<file>    kFP_classifer.py
<brief>   fingerprint using RF, classifiation using kNN
"""

import numpy as np
import multiprocessing as mp
from sklearn.ensemble import RandomForestClassifier

# k-FP's hyperparameters: 
NUM_TREES = 1000
K = 3

def train_kfp(X_train, y_train, trees=NUM_TREES):
    model = RandomForestClassifier(n_jobs=-1, n_estimators=trees, oob_score=True)
    model.fit(X_train, y_train)

    fingerprints = model.apply(X_train)
    labeled_fps = [[fingerprints[i], y_train[i]] for i in range(len(fingerprints))]

    return model, labeled_fps


def test_kfp(model, labeled_fps, X_test):
    test_fps = model.apply(X_test)

    params = [[labeled_fps, test_fp] for test_fp in test_fps]
    with mp.Pool(mp.cpu_count()) as pool:
        pred_labels = pool.starmap(knn_classifier, params)

    return pred_labels


def knn_classifier(labeled_fps, test_fp, k=K):
    test_fp = np.array(test_fp, dtype=np.int32)
        
    hamming_dists=[]

    for e in labeled_fps:
        train_fp = np.array(e[0], dtype=np.int32)
        fp_label = e[1]

        hamming_distance = np.sum(test_fp != train_fp) / float(train_fp.size)

        if hamming_distance == 1.0:
                 continue

        hamming_dists.append((hamming_distance, fp_label))


    by_distance = sorted(hamming_dists)
    k_nearest_labels = [p[1] for p in by_distance[:k]]
    majority_vote = max(set(k_nearest_labels), key=k_nearest_labels.count)

    return majority_vote
