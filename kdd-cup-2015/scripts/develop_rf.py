#!/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import time
import json
import thread
import logging

import numpy as np
import pandas as pd

from collections import OrderedDict
from multiprocessing import Process

from sklearn.metrics import roc_auc_score
from sklearn.metrics import log_loss
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import ParameterGrid
from sklearn.cross_validation import StratifiedShuffleSplit

def load_data(path):

    logger = logging.getLogger("load_data")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    logger.info("load data %r start ... ", path)
    data = pd.read_csv(path).values
    logger.info("data.shape = %r", data.shape)
    logger.info("load data %r end.", path)
    return data

def load_test_data():

    logger = logging.getLogger("load_test_data")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    test_data = load_data("../data/test_data.csv")
    
    id_test = test_data[:, 0]
    X_test = test_data[:, 1:]
    logger.info("X_test.shape = %r", X_test.shape)
    logger.info("load data end ...")
    
    return id_test, X_test

def load_train_data():

    logger = logging.getLogger("load_train_data")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    train_data = load_data("../data/train_data.csv")
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

def make_submission(classifier, parma_dict, filename="submission"):

    logger = logging.getLogger("make_submission")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    id_test, X_test = load_test_data()

    logger.info("predict start ...")
    y_test_proba = classifier.predict_proba(X_test)
    logger.info("y_test_proba.shape = %r", y_test_proba.shape)
    logger.info("predict end.")

    path = "../data/%s.csv" % filename
    submission = pd.DataFrame({"enrollment_id": id_test, "dropout": y_test_proba[:, -1]})
    
    logger.info("dump %s start ...", path)
    submission.to_csv(path, columns = ["enrollment_id", "dropout"], header=False, index=False)
    logger.info("dump %s end.", path)
    
def train_validate_test(param_dict):

    logger = logging.getLogger("develop")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    X_train, X_validate, y_train, y_validate = load_train_data()

    logger.info("train start ... ")
    classifier = RandomForestClassifier(
        n_estimators = param_dict["n_estimators"],
        criterion = param_dict["criterion"],
        max_features = param_dict["max_features"],
        max_depth = param_dict["max_depth"],
        min_samples_split = param_dict["min_samples_split"],
        min_samples_leaf = param_dict["min_samples_leaf"],
        min_weight_fraction_leaf = param_dict["min_weight_fraction_leaf"],
        max_leaf_nodes = param_dict["max_leaf_nodes"],
        bootstrap = param_dict["bootstrap"],
        oob_score = param_dict["oob_score"],
        n_jobs = param_dict["n_jobs"],
        random_state = param_dict["random_state"],
        verbose = param_dict["verbose"],
        warm_start = param_dict["warm_start"],
        class_weight = param_dict["class_weight"]
    )
    classifier.fit(X_train, y_train)
    logger.info("train end.")
    
    logger.info("predict start ...")
    y_train_pred = classifier.predict(X_train)
    y_train_proba = classifier.predict_proba(X_train)
    y_validate_pred = classifier.predict(X_validate)
    y_validate_proba = classifier.predict_proba(X_validate)
    acc_train = accuracy_score(y_train, y_train_pred)
    auc_train = roc_auc_score(y_train, y_train_proba[:, -1])
    logloss_train = log_loss(y_train, y_train_proba)
    acc_validate = accuracy_score(y_validate, y_validate_pred)
    auc_validate = roc_auc_score(y_validate, y_validate_proba[:, -1])
    logloss_validate = log_loss(y_validate, y_validate_proba)
    logger.info("training set auc: %r", auc_train)
    logger.info("validateion set auc: %r", auc_validate)
    logger.info("predict end.")

    timestamp = time.strftime("[%Y-%m-%d]_[%H-%M-%S]", time.localtime(time.time()))
    filename = "submission_rf_%s_[%d]_[%d]" % (timestamp, os.getpid(), thread.get_ident())
    path = "../data/%s.json" % filename
    
    meta = OrderedDict()
    meta["model"] = "RandomForest"
    meta["param_dict"] = param_dict
    meta["acc_train"] = acc_train
    meta["acc_validate"] = acc_validate
    meta["logloss_train"] = logloss_train
    meta["logloss_validate"] = logloss_validate
    meta["auc_train"] = auc_train
    meta["auc_validate"] = auc_validate
    
    logger.info("dump %s start ...", path)
    with open(path, 'w') as fp:
        json.dump(meta, fp, indent=4)
    logger.info("dump %s end.", path)

    make_submission(classifier, param_dict, filename=filename)

def develop():

    param_grid = [
        {
            "n_estimators"             : [200],
            "criterion"                : ["gini"],
            "max_features"             : ["auto", "sqrt", "log2"],
            "max_depth"                : [None],
            "min_samples_split"        : [5, 10, 15, 20], #[25, 50],
            "min_samples_leaf"         : [5, 10, 15, 20], #[25, 30, 35, 40, 45, 50, 55],
            "min_weight_fraction_leaf" : [0.0],
            "max_leaf_nodes"           : [None],
            "bootstrap"                : [True],
            "oob_score"                : [False],
            "n_jobs"                   : [-1],
            "random_state"             : [None],
            "verbose"                  : [0],
            "warm_start"               : [False],
            "class_weight"             : [None],
        }
    ]
    param_list = list(ParameterGrid(param_grid))
    
    process_list = []
    for param_dict in param_list:
        process = Process(target=train_validate_test,
                          args=(param_dict, ))
        process_list.append(process)

    for process in process_list:
        process.start()

    for process in process_list:
        process.join()

def main():

    develop()

if __name__ == "__main__":

    main()
