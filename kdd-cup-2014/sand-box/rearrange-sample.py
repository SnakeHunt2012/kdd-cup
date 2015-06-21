#!/usr/bin/env python
#-*- coding: utf-8 -*-
# rearrange-sample.py

import argparse

if __name__ == "__main__":
    '''
    rearrange sample file into a readable format
    '''
    records = [] # a list of list of entry
    
    # parse arguments and options
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type = str,
                        help = "input file")
    args = parser.parse_args()

    # read in lines from file
    try:
        file_in = open(args.file)
    except IOError:
        print "Couldn't open file %s" % file
    lines = file_in.readlines()
    file_in.close()

    # rearrange entries
    for line in lines:
        if line.isspace():
            continue
        line_rstripped = line.strip()
        list_entry = line_rstripped.split(',')
        records.append(list_entry[:])

    # print entries rearranged
    length_row = len(records)
    length_col = len(records[0])
    for index_col in range(length_col):
        for index_row in range(length_row):
            print "%s\n" % records[index_row][index_col],
        print

