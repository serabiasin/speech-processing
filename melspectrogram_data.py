#! /usr/env/bin python3
import sys
import os
import scipy.io.wavfile as wav
import scipy.signal
import numpy as np
import librosa
import argparse


def readFile(file):
  vector,fs=librosa.load(file,sr=16000,mono=True)
  return vector,fs

def dynamic_range_compress(spect,konstanta=10000):
  return np.log(np.multiply(konstanta,spect)+1)

def getSpectrogram(vector,fs):
  return dynamic_range_compress(librosa.feature.melspectrogram(y=vector, sr=fs,n_fft=1024,hop_length=160))



direktori_root=""

parser = argparse.ArgumentParser(description='Tools untuk membuat Noise pada file wav')
parser.add_argument('--dir', help="Target Direktori ")

args = parser.parse_args()
Direktori=args.dir

sub_dir=[]
X=[]
Y=[]
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
            #extraction feature
            print(os.path.join(buffer,data))
            vector,fs=readFile(os.path.join(buffer,data))
            spec=getSpectrogram(vector,fs)
            X.append(spec[:,:100])
            Y.append(sub_dir[index])

print(np.asarray(X).shape)
print(np.asarray(Y))

Y=np.asarray(Y)
X=np.asarray(X)
Direktori="/content/drive/My Drive/percobaan/"
np.save(Direktori+'/data_latihSpectro'+'.npy',X)
np.save(Direktori+'labelSpectro'+'.npy',Y)
print("done")
