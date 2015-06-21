#!/bin/bash
# develop.sh

# dirs
script_dir=$(pwd)
log_dir=${script_dir}/../log

# paths
pyscript_path=${script_dir}/develop.py
log_path=${log_dir}/develop.log

# develop
python ${pyscript_path} > ${log_path}

