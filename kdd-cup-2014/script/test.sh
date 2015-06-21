#!/bin/bash
# test.sh

# dirs
script_dir=$(pwd)
log_dir=${script_dir}/../log

# paths
pyscript_path=${script_dir}/test.py
log_path=${log_dir}/test.log

# test
python ${pyscript_path} > ${log_path}