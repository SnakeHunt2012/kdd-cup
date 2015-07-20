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

from sklearn.svm import SVC
from sklearn.metrics import log_loss
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.grid_search import ParameterGrid
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import StratifiedShuffleSplit

scaler_dict = {
    "StandardScaler" : StandardScaler,
    "MinMaxScaler" : MinMaxScaler
}

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

def load_test_data(scaler):

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

    if scaler is not None:
        X_test = scaler.transform(X_test.astype(np.float))
    else:
        X_test = X_test.astype(np.float)
    
    logger.info("X_test.shape = %r", X_test.shape)
    logger.debug("X_test = %r", X_test)
    logger.info("id_test.shape = %r", id_test.shape)
    logger.debug("id_test = %r", id_test)
    logger.info("load data end ...")
    
    return id_test, X_test

def load_train_data(scaler):

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

    scaler = scaler_dict[scaler]() if scaler in scaler_dict else scaler
    logger.info("Using scaler: %r", scaler.__class__)
    if scaler is not None:
        scaler.fit(X_train.astype(np.float))
        X_train = scaler.transform(X_train.astype(np.float))
        X_validate = scaler.transform(X_validate.astype(np.float))
        logger.info("Scaler params: %r", scaler.get_params(deep=False))
        logger.debug("Scaler params: %r", scaler.get_params(deep=True))
    else:
        X_train = X_train.astype(np.float)
        X_validate = X_validate.astype(np.float)
    
    logger.info("X_train.shape = %r", X_train.shape)
    logger.debug("X_train = %r", X_train)
    logger.info("X_validate.shape = %r", X_validate.shape)
    logger.debug("X_validate = %r", X_validate)
    logger.info("y_train.shape = %r", y_train.shape)
    logger.debug("y_train = %r", y_train)
    logger.info("y_validate.shape = %r", y_validate.shape)
    logger.debug("y_validate = %r", y_validate)
    logger.info("load data end.")

    return X_train, X_validate, y_train, y_validate, scaler

def make_submission(classifier, scaler, parma_dict, filename="submission"):

    logger = logging.getLogger("make_submission")
    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    id_test, X_test = load_test_data(scaler)

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

    X_train, X_validate, y_train, y_validate, scaler = load_train_data(param_dict["scaler"])

    logger.info("train start ... ")
    classifier = SVC(
        C = param_dict["C"],
        kernel = param_dict["kernel"],
        degree = param_dict["degree"],
        gamma = param_dict["gamma"],
        coef0 = param_dict["coef0"],
        probability = param_dict["probability"],
        shrinking = param_dict["shrinking"],
        tol = param_dict["tol"],
        cache_size = param_dict["cache_size"],
        class_weight = param_dict["class_weight"],
        verbose = param_dict["verbose"],
        max_iter = param_dict["max_iter"],
        random_state = param_dict["random_state"]
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
    filename = "submission_svm_%s_[%d]_[%d]" % (timestamp, os.getpid(), thread.get_ident())
    path = "../data/%s.json" % filename
    
    meta = OrderedDict()
    meta["model"] = "SVM"
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

    make_submission(classifier, scaler, param_dict, filename=filename)

def develop():

    param_grid = [
        {   # rbf: C overfit, gamma underfit
            "scaler" : ["StandardScaler"], # this is framework featured parameter, not belongs to the model
            "C" : [1.1, 1.5, 2.0], # >1. overfit
            "kernel" : ["rbf"],
            "degree" : [3], # Note: Degree of the polynomial kernel function ('poly'), ignored by all other kernels.
            "gamma" : [0.02, 0.015, 0.01, 0.005], # <.03 underfit
            "coef0" : [0.0], # Note: It is only significant in 'poly' and 'sigmoid'.
            "probability" : [True],
            "shrinking" : [True],
            "tol" : [1e-3],
            "cache_size" : [1024],
            "class_weight" : ["auto"],
            "verbose" : [False],
            "max_iter" : [-1],
            "random_state" : [None]
        },
        {   # rbf: C underfit, gamma overfit
            "scaler" : ["StandardScaler"], # this is framework featured parameter, not belongs to the model
            "C" : [0.5, 0.55, 0.6, 0.65], # <1. underfit
            "kernel" : ["rbf"],
            "degree" : [3], # Note: Degree of the polynomial kernel function ('poly'), ignored by all other kernels.
            "gamma" : [0.01, 0.015, 0.02, 0.025], # >.03 overfit
            "coef0" : [0.0], # Note: It is only significant in 'poly' and 'sigmoid'.
            "probability" : [True],
            "shrinking" : [True],
            "tol" : [1e-3],
            "cache_size" : [1024],
            "class_weight" : ["auto"],
            "verbose" : [False],
            "max_iter" : [-1],
            "random_state" : [None]
        },
        {   # poly
            "scaler" : ["StandardScaler"], # this is framework featured parameter, not belongs to the model
            "C" : [0.7, 0.9, 1.1, 1.5],
            "kernel" : ["poly"],
            "degree" : [4, 5], # Note: Degree of the polynomial kernel function ('poly'), ignored by all other kernels.
            "gamma" : [0.01, 0.015, 0.02, 0.025],
            "coef0" : [0.0], # Note: It is only significant in 'poly' and 'sigmoid'.
            "probability" : [True],
            "shrinking" : [True],
            "tol" : [1e-3],
            "cache_size" : [1024],
            "class_weight" : ["auto"],
            "verbose" : [False],
            "max_iter" : [-1],
            "random_state" : [None]
        },
        {   # linear
            "scaler" : ["StandardScaler"], # this is framework featured parameter, not belongs to the model
            "C" : [0.9, 1.1, 1.5, 2, 2.5],
            "kernel" : ["linear"],
            "degree" : [3], # Note: Degree of the polynomial kernel function ('poly'), ignored by all other kernels.
            "gamma" : [0.02, 0.025, 0.3, 0.035],
            "coef0" : [0.0], # Note: It is only significant in 'poly' and 'sigmoid'.
            "probability" : [True],
            "shrinking" : [True],
            "tol" : [1e-3],
            "cache_size" : [1024],
            "class_weight" : ["auto"],
            "verbose" : [False],
            "max_iter" : [-1],
            "random_state" : [None]
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
