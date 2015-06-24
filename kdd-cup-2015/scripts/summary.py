#!/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import json

def summary_svm(cmd="ls ../data/submission_svm_*.json"):

    with os.popen(cmd) as fp:
        file_list = fp.read().split()

    json_list = []
    for json_file in file_list:
        with open(json_file, 'r') as fp:
            json_list.append((json_file, json.loads(fp.read())))
    json_list.sort(key=lambda (json_file, json_dict):
                   (json_dict["param_dict"]["scaler"],
                    json_dict["param_dict"]["kernel"],
                    json_dict["param_dict"]["class_weight"]))

    output_format = "%f\t%f\t%s\t%s\t%s\t%s"
    print ""
    for json_file, json_dict in json_list:
        print output_format % \
            (
                json_dict["auc_validate"],
                json_dict["auc_train"] - json_dict["auc_validate"],
                json_dict["param_dict"]["scaler"],
                json_dict["param_dict"]["kernel"],
                json_dict["param_dict"]["class_weight"],
                json_file
            )

def summary_gb(cmd="ls ../data/submission_gb_*.json"):

    with os.popen(cmd) as fp:
        file_list = fp.read().split()

    json_list = []
    for json_file in file_list:
        with open(json_file, 'r') as fp:
            json_list.append((json_file, json.loads(fp.read())))
    json_list.sort(key=lambda (json_file, json_dict):
                   (json_dict["param_dict"]["loss"],
                    json_dict["param_dict"]["max_depth"],
                    json_dict["param_dict"]["min_samples_leaf"]))

    output_format = "%f\t%f\t%s\t%d\t%d\t%s"
    print "auc_validate\ttrain - validate\tmin_samples_leaf\tmin_samples_split\tfile"
    for json_file, json_dict in json_list:
        print output_format % \
            (
                json_dict["auc_validate"],
                json_dict["auc_train"] - json_dict["auc_validate"],
                json_dict["param_dict"]["loss"],
                json_dict["param_dict"]["max_depth"],
                json_dict["param_dict"]["min_samples_leaf"],
                json_file
            )

def summary_rf(cmd="ls ../data/submission_rf_*.json"):

    with os.popen(cmd) as fp:
        file_list = fp.read().split()

    json_list = []
    for json_file in file_list:
        with open(json_file, 'r') as fp:
            json_list.append((json_file, json.loads(fp.read())))
    json_list.sort(key=lambda (json_file, json_dict):
                   (json_dict["param_dict"]["criterion"],
                    json_dict["param_dict"]["min_samples_leaf"],
                    json_dict["param_dict"]["min_samples_split"]))

    output_format = "%f\t%f\t%d\t%d\t%s\t%s"
    print "auc_validate\ttrain - validate\tmin_samples_leaf\tmin_samples_split\tcriterion"
    for json_file, json_dict in json_list:
        print output_format % \
            (
                json_dict["auc_validate"],
                json_dict["auc_train"] - json_dict["auc_validate"],
                json_dict["param_dict"]["min_samples_leaf"],
                json_dict["param_dict"]["min_samples_split"],
                json_dict["param_dict"]["criterion"],
                json_file
            )

def main():

    #summary_rf()
    #summary_gb("ls ../data/submission_gb_*.json")
    summary_svm("ls ../data/submission_svm_*.json")

if __name__ == "__main__":

    main()
