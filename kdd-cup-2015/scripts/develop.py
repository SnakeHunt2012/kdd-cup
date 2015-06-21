#!/bin/env python2.7

import logging

import numpy as np
import pandas as pd

from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

def load_train_data():

    logger = logging.getLogger("load_train_data")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    logger.info("load data begin ... ")
    train_data = pd.read_csv("../data/train_data.csv").values
    np.random.shuffle(train_data)

    sss = StratifiedShuffleSplit(train_data[:, -1], test_size=0.2, n_iter=1)
    train_index, validate_index = iter(sss).next()

    X_train = train_data[train_index, 1:-1]
    X_validate = train_data[validate_index, 1:-1]
    y_train = train_data[train_index, -1]
    y_validate = train_data[validate_index, -1]
    logger.info("X_train.shape = %r", X_train.shape)
    logger.info("X_validate.shape = %r", X_validate.shape)
    logger.info("y_train.shape = %r", y_train.shape)
    logger.info("y_validate.shape = %r", y_validate.shape)
    logger.info("load data end.")


    return X_train, X_validate, y_train, y_validate

def develop():

    logger = logging.getLogger("develop")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    train_data = pd.read_csv("../data/train_data.csv").values
    np.random.shuffle(train_data)

    X_train, X_validate, y_train, y_validate = load_train_data()

    logger.info("train start ... ")
    classifier = RandomForestClassifier(
        n_estimators = 100,
        criterion = "gini",
        max_features = None,
        max_depth = None,
        min_samples_split = 2,
        min_samples_leaf = 2,
        min_weight_fraction_leaf = 0.0,
        max_leaf_nodes = None,
        bootstrap = True,
        oob_score = False,
        n_jobs = -1,
        random_state = None,
        verbose = 0,
        warm_start = False,
        class_weight = None,
    )
    classifier.fit(X_train, y_train)
    logger.info("train end.")
    
    logger.info("predict start ...")
    y_train_pred = classifier.predict_proba(X_train)
    y_validate_pred = classifier.predict_proba(X_validate)
    logger.info("training set auc: %r", roc_auc_score(y_train, y_train_pred[:, 1]))
    logger.info("validateion set auc: %r", roc_auc_score(y_validate, y_validate_pred[:, 1]))
    logger.info("predict end.")

def main():

    develop()

if __name__ == "__main__":

    main()
