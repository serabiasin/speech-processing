#! /usr/env/bin python3

import argparse
import os
import sys
import glob
import pickle
import numpy as np
import scipy
import librosa


"""
generateNoise
@parameter

file : file yang akan di augmentasi data nya
const -> konstanta yang berperan sebagai scalar vector untuk membuat noise

@deskripsi
membuat noise dari satu buah file

"""
def generateNoise(dataSuara,const=0.005):
  dataSuara=dataSuara.astype('float32')
  noise=np.random.normal(size=len(dataSuara))
  dataModif=dataSuara+const*noise
  #normalisasi
  m = np.max(np.abs(dataModif))
  dataModif = (dataModif/m).astype(np.float32)

  return dataModif



"""
readFile

@parameter
path  -> lokasi wav file

@deskripsi :
mengubah file binary wav menjadi vector

@return value :
float32 dalam bentuk vector
"""

def readFile(path):
    return scipy.io.wavfile.read(path)


"""
vecTofile

@parameter

targetPath      -> target Direktori

fileName        -> nama file yang akan di augmentasi

sekuen          -> merupakan proses ke - n dari augmentasi

data            -> data vector yang telah di augmentasi oleh noise generator

samplingRate    -> frame Rate dari sebuah data wav

@deskripsi :
mengubah data Vector menjadi sebuah file wav


"""
def vecTofile(targetPath,fileName,sekuen,data,samplingRate=16000):
  namafile=fileName+'-'+str(sekuen)+'.wav'
  target=os.path.join(targetPath,namafile)
  print("File : ",fileName," Created : "," To : ",namafile)
  scipy.io.wavfile.write(target, samplingRate, data)


"""
beginProcess

@parameter

direktori       -> target direktori yang akan di augmentasi

namafile        -> nama file yang akan di augmentasi

@deskripsi :
membuat noise dari satu buah file

"""
def beginProcess(direktori,namaFile):
  target=os.path.join(direktori,namaFile)
  for sequence in range(1,201):
    #avoid overflow,using random constant instead linear constant
    konstanta=np.random.randint(low=10.05, high=90.5, size=1)
    #bikin noise
    print(target)
    sr,buffer=readFile(target)
    if sr==16000:
      hasil=generateNoise(buffer,konstanta)
      #tulis file
      vecTofile(direktori,namaFile[:-4],sequence,hasil)
    else:
      print("Gagal Melakukan Proses (Sampling rate harus 16KHz)")
      print("Error File at :",target)
      break


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
            # disini buat proses noise generator
            beginProcess(buffer,data)
