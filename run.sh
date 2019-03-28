#!/bin/bash 
. /pbs/home/c/cbernet/miniconda3/etc/profile.d/conda.sh
conda activate k80
# script='python /pbs/home/c/cbernet/deeplearning/maldives/imdb/imdb_convnet.py'
script='python /pbs/home/c/cbernet/deeplearning/maldives/yelp/yelp_lstm.py'
args=''
exec $script $args
