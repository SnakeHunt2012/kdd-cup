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
from sklearn.ensemble import GradientBoostingClassifier
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
    y_test_pred = classifier.predict_proba(X_test)
    logger.info("y_test_pred.shape = %r", y_test_pred.shape)
    logger.info("predict end.")

    path = "../data/%s.csv" % filename
    submission = pd.DataFrame({"enrollment_id": id_test, "dropout": y_test_pred[:, -1]})
    
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
    classifier = GradientBoostingClassifier(
        loss = param_dict["loss"],
        learning_rate = param_dict["learning_rate"],
        n_estimators = param_dict["n_estimators"],
        max_depth = param_dict["max_depth"],
        min_samples_split = param_dict["min_samples_split"],
        min_samples_leaf = param_dict["min_samples_leaf"],
        min_weight_fraction_leaf = param_dict["min_weight_fraction_leaf"],
        subsample = param_dict["subsample"],
        max_features = param_dict["max_features"],
        max_leaf_nodes = param_dict["max_leaf_nodes"],
        init = param_dict["init"],
        verbose = param_dict["verbose"],
        warm_start = param_dict["warm_start"]
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
    logloss_train = log_loss(y_train, y_train_pred)
    acc_validate = accuracy_score(y_validate, y_validate_pred)
    auc_validate = roc_auc_score(y_validate, y_validate_proba[:, -1])
    logloss_validate = log_loss(y_validate, y_validate_pred)
    logger.info("training set auc: %r", auc_train)
    logger.info("validateion set auc: %r", auc_validate)
    logger.info("predict end.")

    timestamp = time.strftime("[%Y-%m-%d]_[%H-%M-%S]", time.localtime(time.time()))
    filename = "submission_gb_%s_[%d]_[%d]" % (timestamp, os.getpid(), thread.get_ident())
    path = "../data/%s.json" % filename
    
    meta = OrderedDict()
    meta["model"] = "GradientBoosting"
    meta["param_dict"] = param_dict
    meta["acc_train"] = acc_train
    meta["auc_train"] = auc_train
    meta["logloss_train"] = logloss_train
    meta["acc_validate"] = acc_validate
    meta["auc_validate"] = auc_validate
    meta["logloss_validate"] = logloss_validate
    
    logger.info("dump %s start ...", path)
    with open(path, 'w') as fp:
        json.dump(meta, fp, indent=4)
    logger.info("dump %s end.", path)

    make_submission(classifier, param_dict, filename=filename)

def develop():

    param_grid = [
        #{
        #    "loss"                     : ["deviance"], # ???
        #    "learning_rate"            : [0.1], # ??? There is a trade-off between learning_rate and n_estimators.
        #    "n_estimators"             : [100],
        #    "max_depth"                : [3, 4, 5, 6, 7], # Ignored if ``max_leaf_nodes`` is not None.
        #    "min_samples_split"        : [2, 6, 10],
        #    "min_samples_leaf"         : [20, 25, 30, 35, 40, 45, 50],
        #    "min_weight_fraction_leaf" : [0.0],
        #    "subsample"                : [1.0],
        #    "max_features"             : [None],
        #    "max_leaf_nodes"           : [None],
        #    "init"                     : [None], # ???
        #    "verbose"                  : [1],
        #    "warm_start"               : [False]
        #},
        {
            "loss"                     : ["deviance"], # ???
            "learning_rate"            : [0.1], # ??? There is a trade-off between learning_rate and n_estimators.
            "n_estimators"             : [100],
            "max_depth"                : [100], # Ignored if ``max_leaf_nodes`` is not None.
            "min_samples_split"        : [10],
            "min_samples_leaf"         : range(460, 710, 10),
            "min_weight_fraction_leaf" : [0.0],
            "subsample"                : [1.0],
            "max_features"             : [None],
            "max_leaf_nodes"           : [None],
            "init"                     : [None], # ???
            "verbose"                  : [1],
            "warm_start"               : [False]
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
