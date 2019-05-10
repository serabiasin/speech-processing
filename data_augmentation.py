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

file    ->    file yang akan di augmentasi data nya
const   ->    konstanta yang berperan sebagai scalar vector untuk membuat noise

@deskripsi
membuat noise dari satu buah file

"""
def generateNoise(dataSuara,const=0.005):
  dataSuara=dataSuara.astype('float32')
  noise=np.random.normal(loc=0.2,size=len(dataSuara))
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
  print("File : ",fileName," Created : "," To : ",target)
  scipy.io.wavfile.write(target, samplingRate, data)


"""
addReverbEffect

@parameter

dataSuara           ->  dataSuara berupa vector

hfdampingConst      ->  konstanta high frequency damping

reverbConst         ->  konstanta reverbation

room_scaleConst     ->  konstanta untuk visualisasi skala ruangan
                        (ukuran ruangan)

gainConst           ->  konstanta untuk melakukan penguatan atau pelemahan
                        range (-10 hingga 10 dB)

@deskripsi  :
proses penambahan efek reverb

@return value :
berupa nilai vektor,hasil efek manipulasi reverb dengan
parameter yang telah disediakan

"""
def addReverbEffect(dataSuara,hfdampingConst,reverbConst,room_scaleConst,gainConst=0):
  fx = (AudioEffectsChain().reverb( hf_damping=hfdampingConst,
                                   room_scale=room_scaleConst,
                                   reverberance=reverbConst,wet_gain=gainConst))

  return fx(dataSuara)


"""
reverbanceAugmentation

@parameter

direktori           -> target Direktori

namaFile            -> nama file

@deskripsi

Proses melakukan pemindaian file dan direktori,setelah diperoleh data direktori
akan dilakukan proses manipulasi efek oleh fungsi addReverbEffect,setelah
diperoleh nilai vektor dari fungsi tersebut akan di konversi menjadi file
berformat wav

"""
def reverbanceAugmentation(direktori,namaFile):
  target=os.path.join(direktori,namaFile)
  for sequence in range(0,50):
    sr,buffer=readFile(target)
    hfdampingConst=np.random.uniform(low=10, high=100)
    reverbConst=np.random.uniform(low=10, high=100)
    room_scaleConst=np.random.uniform(low=10, high=100)
    gainConst=np.random.uniform(low=1, high=10)
    if sr==16000:
      hasil=addReverbEffect(buffer,hfdampingConst,reverbConst,room_scaleConst,gainConst)
      vecTofile(direktori,namaFile[:-4],sequence,hasil)
    else:
      print("Gagal Melakukan Proses..")
      print("Error File at : ",target)
      break

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
  for sequence in range(0,10):
    #avoid overflow,using random constant instead linear constant
    konstanta=np.random.uniform(low=10, high=95)
    #bikin noise
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

#white noise addition
for index in range(len(sub_dir)):
    print(sub_dir[index])
    for data in os.listdir(os.path.join(Direktori,sub_dir[index])):
        buffer=os.path.join(Direktori,sub_dir[index])
        if os.path.isfile(os.path.join(buffer,data)):
            beginProcess(buffer,data)

# Reverb Noise addition
for index in range(len(sub_dir)):
    print(sub_dir[index])
    for data in os.listdir(os.path.join(Direktori,sub_dir[index])):
        buffer=os.path.join(Direktori,sub_dir[index])
        if os.path.isfile(os.path.join(buffer,data)):
            reverbanceAugmentation(buffer,data)
