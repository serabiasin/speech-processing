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

def readFile(arg):
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
    elif os.path.isfile(os.path.join(Direktori,folder)):
        pass

for index in range(len(sub_dir)):
    print(sub_dir[index])
    for data in os.listdir(os.path.join(Direktori,sub_dir[index])):
        buffer=os.path.join(Direktori,sub_dir[index])
        if os.path.isfile(os.path.join(buffer,data)):
            print(os.path.join(buffer,data))
            # disini buat proses noise generator
            
