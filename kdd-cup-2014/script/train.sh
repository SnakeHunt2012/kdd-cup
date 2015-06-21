#!/bin/bash
# train.sh

# dirs
script_dir=$(pwd)
log_dir=${script_dir}/../log

# paths
pyscript_path=${script_dir}/train.py
log_path=${log_dir}/train.log

# train
python ${pyscript_path} > ${log_path}

