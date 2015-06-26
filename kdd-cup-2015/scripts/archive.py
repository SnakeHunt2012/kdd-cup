#!/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import json
import logging
import argparse

from subprocess import check_output
from subprocess import check_call

def archive_directory(json_file, target):

    csv_file = os.path.splitext(json_file)[0] + ".csv"
    target_directory = "../data/%s" % target

    check_call("mkdir --parents %s" % target_directory, shell=True)
    check_call("mv %s %s/" % (json_file, target_directory), shell=True)
    check_call("mv %s %s/" % (csv_file, target_directory), shell=True)

def archive_database(json_dict, target):

    pass

def archive(json_file, target):

    print "archive %s -> %s ..." % (json_file, target),

    with open(json_file, 'r') as fp:
        json_dict = json.loads(fp.read())

    archive_database(json_dict, target)
    archive_directory(json_file, target)
    
    print "done."

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="target directory, such as '2015-06-26'")
    args = parser.parse_args()
    target = args.target

    output = check_output("ls ../data/submission_*.json", shell=True)
    file_list = output.strip().split("\n")

    for json_file in file_list:
        archive(json_file, target)

if __name__ == "__main__":

    main()
