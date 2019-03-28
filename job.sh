#!/bin/bash 
/usr/bin/singularity exec --nv --bind /pbs:/pbs --bind /sps:/sps /cvmfs/singularity.in2p3.fr/images/HPC/GPU/centos7_cuda9-2_cudnn7-3_nccl2-2-12.simg ~/deeplearning/submission/run.sh
