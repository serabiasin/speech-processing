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
for folder in os.listdir(Direktori):
    if os.path.isdir(os.path.join(Direktori,folder)):
        sub_dir.append(folder)
    elif os.path.isfile(folder):
        pass

print(sub_dir)
