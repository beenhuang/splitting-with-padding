#!/usr/bin/env python3

"""
<file>    kFP_classifer.py
<brief>   fingerprint using RF, classifiation using kNN
"""

import sys
import numpy as np
import multiprocessing as mp

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_kfp(X_train, y_train, trees=1000):
    model = RandomForestClassifier(n_jobs=-1, n_estimators=trees, oob_score=True)
    model.fit(X_train, y_train)

    fingerprints = model.apply(X_train)
    labeled_fps = [[fingerprints[i], y_train[i]] for i in range(len(fingerprints))]

    return model, labeled_fps


def test_kfp(model, labeled_fps, X_test):
    pred_labels = []

    new_fps = model.apply(X_test)

    argus = [[labeled_fps, new_fp] for new_fp in new_fps]

    with mp.Pool(mp.cpu_count()) as pool:
        pred_labels = pool.starmap(knn_classifier, argus)

    return pred_labels


def knn_classifier(labeled_fps, new_fp, k=3):
    new_fp = np.array(new_fp, dtype=np.int32)
        
    hamming_dists=[]

    for elem in labeled_fps:
        labeled_fp = np.array(elem[0], dtype=np.int32)
        pred_label = elem[1]

        hamming_distance = np.sum(new_fp != labeled_fp) / float(labeled_fp.size)

        if hamming_distance == 1.0:
                 continue

        hamming_dists.append((hamming_distance, pred_label))


    by_distance = sorted(hamming_dists)
    k_nearest_labels = [p[1] for p in by_distance[:k]]
    majority_vote = max(set(k_nearest_labels), key=k_nearest_labels.count)


    return majority_vote
