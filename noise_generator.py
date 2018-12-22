#! /usr/env/bin python3

import muda
import argparse
import os
import sys
import glob
import pickle
import numpy as np


"""
generateNoise
deskripsi :
membuat noise dari satu buah file

parameter
file : file yang akan di augmentasi data nya


"""
# Implemented Soon
def generateNoise(file):
    pass


direktori_root=""

parser = argparse.ArgumentParser(description='Tools untuk membuat Noise pada file wav')
parser.add_argument('--dir', help="Target Direktori ")

args = parser.parse_args()
Direktori=args.dir

sub_dir=[]
for file in os.listdir(Direktori):
    if os.path.isdir(file):
        sub_dir.append(file)

print(range(sub_dir))
# for sub_dir in variable:
#     pass
