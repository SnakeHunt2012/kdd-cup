#!/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import json

def summary():

    with os.popen("ls ../data/submission_rf_*.json") as fp:
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

    summary()

if __name__ == "__main__":

    main()
