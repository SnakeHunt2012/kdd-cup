#!/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import json
import logging
import argparse

from subprocess import check_call
from subprocess import check_output

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, BigInteger, Float, String, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://admin@localhost/kdd-cup-2015', echo=True)
Base = declarative_base()

class RF_Meta(Base):

    __tablename__ = "rf_meta"

    # json_file
    model = Column(String, primary_key=True)
    timestamp = Column(TIMESTAMP, primary_key=True)
    pid = Column(Integer, primary_key=True)
    tid = Column(BigInteger, primary_key=True)

    # json_dict["param_dict"]
    warm_start = Column(Boolean)
    oob_score = Column(Boolean)
    n_jobs = Column(Integer)
    max_leaf_nodes = Column(Integer);
    bootstrap = Column(Boolean);
    min_samples_leaf = Column(Integer);
    n_estimators = Column(Integer);
    min_samples_split = Column(Integer);
    min_weight_fraction_leaf = Column(Float);
    criterion = Column(Float);
    random_state = Column(Integer);
    max_features = Column(String);
    max_depth = Column(Integer);
    class_weight = Column(String);

    # json_dict
    acc_train = Column(Float);
    acc_validate = Column(Float);
    logloss_train = Column(Float);
    logloss_validate = Column(Float);
    auc_train = Column(Float);
    auc_validate = Column(Float);

    # json_file
    target = Column(String);
    filename = Column(String);

class GB_Meta(Base):

    __tablename__ = "gb_meta"

    # json_file
    model = Column(String, primary_key=True)
    timestamp = Column(TIMESTAMP, primary_key=True)
    pid = Column(Integer, primary_key=True)
    tid = Column(BigInteger, primary_key=True)

    # json_dict["param_dict"]
    loss = Column(String);
    subsample = Column(Float);
    max_leaf_nodes = Column(Integer);
    learning_rate = Column(Float);
    min_samples_leaf = Column(Integer);
    n_estimators = Column(Integer);
    min_samples_split = Column(Integer);
    init = Column(String);
    min_weight_fraction_leaf = Column(Float);
    max_features = Column(String);
    max_depth = Column(Integer);

    # json_dict
    acc_train = Column(Float);
    acc_validate = Column(Float);
    logloss_train = Column(Float);
    logloss_validate = Column(Float);
    auc_train = Column(Float);
    auc_validate = Column(Float);

    # json_file
    target = Column(String);
    filename = Column(String);

class SVM_Meta(Base):

    __tablename__ = "svm_meta"

    # json_file
    model = Column(String, primary_key=True)
    timestamp = Column(TIMESTAMP, primary_key=True)
    pid = Column(Integer, primary_key=True)
    tid = Column(BigInteger, primary_key=True)

    # json_dict["param_dict"]
    kernel = Column(String);
    c = Column(Float);
    probability = Column(Boolean);
    degree = Column(Integer);
    scaler = Column(String);
    shrinking = Column(Boolean);
    max_iter = Column(Integer);
    random_state = Column(Integer);
    tol = Column(Float);
    cache_size = Column(Integer);
    coef0 = Column(Float);
    gamma = Column(Float);
    class_weight = Column(String);

    # json_dict
    acc_train = Column(Float);
    acc_validate = Column(Float);
    logloss_train = Column(Float);
    logloss_validate = Column(Float);
    auc_train = Column(Float);
    auc_validate = Column(Float);

    # json_file
    target = Column(String);
    filename = Column(String);

def archive_rf(session, date, time, pid, tid, target, filename, json_dict):

    model = json_dict["model"]
    timestamp = date + "T" + time.replace("-", ":")
    param_dict = json_dict["param_dict"]
    
    rf_meta = RF_Meta(
        model=model,
        timestamp=timestamp,
        pid=pid,
        tid=tid,
    
        warm_start=param_dict["warm_start"],
        oob_score=param_dict["oob_score"],
        n_jobs=param_dict["n_jobs"],
        max_leaf_nodes=param_dict["max_leaf_nodes"],
        bootstrap=param_dict["bootstrap"],
        min_samples_leaf=param_dict["min_samples_leaf"],
        n_estimators=param_dict["n_estimators"],
        min_samples_split=param_dict["min_samples_split"],
        min_weight_fraction_leaf=param_dict["min_weight_fraction_leaf"],
        criterion=param_dict["criterion"],
        random_state=param_dict["random_state"],
        max_features=param_dict["max_features"],
        max_depth=param_dict["max_depth"],
        class_weight=param_dict["class_weight"],
    
        acc_train=json_dict["acc_train"],
        acc_validate=json_dict["acc_validate"],
        logloss_train=json_dict["logloss_train"],
        logloss_validate=json_dict["logloss_validate"],
        auc_train=json_dict["auc_train"],
        auc_validate=json_dict["auc_validate"],
    
        target=target,
        filename=filename
    )
    session.add(rf_meta)
    session.commit()

def archive_gb(session, date, time, pid, tid, target, filename, json_dict):

    model = json_dict["model"]
    timestamp = date + "T" + time.replace("-", ":")
    param_dict = json_dict["param_dict"]

    gb_meta = GB_Meta(
        model=model,
        timestamp=timestamp,
        pid=pid,
        tid=tid,
    
        loss=param_dict["loss"],
        subsample=param_dict["subsample"],
        max_leaf_nodes=param_dict["max_leaf_nodes"],
        learning_rate=param_dict["learning_rate"],
        min_samples_leaf=param_dict["min_samples_leaf"],
        n_estimators=param_dict["n_estimators"],
        min_samples_split=param_dict["min_samples_split"],
        init=param_dict["init"],
        min_weight_fraction_leaf=param_dict["min_weight_fraction_leaf"],
        max_features=param_dict["max_features"],
        max_depth=param_dict["max_depth"],
    
        acc_train=json_dict["acc_train"],
        acc_validate=json_dict["acc_validate"],
        logloss_train=json_dict["logloss_train"],
        logloss_validate=json_dict["logloss_validate"],
        auc_train=json_dict["auc_train"],
        auc_validate=json_dict["auc_validate"],
    
        target=target,
        filename=filename
    )
    session.add(gb_meta)
    session.commit()
    
def archive_svm(session, date, time, pid, tid, target, filename, json_dict):

    model = json_dict["model"]
    timestamp = date + "T" + time.replace("-", ":")
    param_dict = json_dict["param_dict"]
    
    svm_meta = SVM_Meta(
        model=model,
        timestamp=timestamp,
        pid=pid,
        tid=tid,
    
        kernel=param_dict["kernel"],
        c=param_dict["C"],
        probability=param_dict["probability"],
        degree=param_dict["degree"],
        scaler=param_dict["scaler"],
        shrinking=param_dict["shrinking"],
        max_iter=param_dict["max_iter"],
        random_state=param_dict["random_state"],
        tol=param_dict["tol"],
        cache_size=param_dict["cache_size"],
        coef0=param_dict["coef0"],
        gamma=param_dict["gamma"],
        class_weight=param_dict["class_weight"],
    
        acc_train=json_dict["acc_train"],
        acc_validate=json_dict["acc_validate"],
        logloss_train=json_dict["logloss_train"],
        logloss_validate=json_dict["logloss_validate"],
        auc_train=json_dict["auc_train"],
        auc_validate=json_dict["auc_validate"],
    
        target=target,
        filename=filename
    )
    session.add(svm_meta)
    session.commit()

def archive_directory(json_file, target):

    csv_file = os.path.splitext(json_file)[0] + ".csv"
    target_directory = "../data/%s" % target

    check_call("mkdir --parents %s" % target_directory, shell=True)
    check_call("mv %s %s/" % (json_file, target_directory), shell=True)
    check_call("mv %s %s/" % (csv_file, target_directory), shell=True)

def archive_database(json_file, session, target):

    file_split = json_file.split("_")
    assert len(file_split) == 6

    model = file_split[1].strip()
    date = file_split[2].strip("[\[\]]")
    time = file_split[3].strip("[\[\]]")
    pid = file_split[4].strip("[\[\]")
    tid = file_split[5].rstrip("\.json").strip("\[\]")
    filename = json_file.split("/")[-1].rstrip(".json")

    with open(json_file, 'r') as fp:
        json_dict = json.loads(fp.read())

    switch_case = {
        "rf" : archive_rf,
        "gb" : archive_gb,
        "svm" : archive_svm,
    }

    assert model in switch_case
    switch_case[model](session, date, time, pid, tid, target, filename, json_dict)

def archive(json_file, session, target):

    print "archive %s -> %s ..." % (json_file, target),

    archive_database(json_file, session, target)
    archive_directory(json_file, target)
    
    print "done."

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="target directory, such as '2015-06-26'")
    args = parser.parse_args()
    target = args.target

    output = check_output("ls ../data/submission_*.json", shell=True)
    file_list = output.strip().split("\n")

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    for json_file in file_list:
        archive(json_file, session, target)

    session.close()

if __name__ == "__main__":

    main()
