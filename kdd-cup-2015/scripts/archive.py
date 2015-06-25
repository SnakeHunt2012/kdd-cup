#!/bin/env python2.7
# -*- coding: utf-8 -*-

import commands

def archive():

    status, output = commands.getstatusoutput("ls ../data/submission_*.json")
    file_list = output.split('\n')
    print len(file_list)

def main():

    archive()

if __name__ == "__main__":

    main()
