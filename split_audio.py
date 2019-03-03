from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import argparse



#based on : https://stackoverflow.com/questions/36799902/how-to-splice-an-audio-file-wav-format-into-1-sec-splices-in-python
root_dir=""

parser = argparse.ArgumentParser(description='Tools untuk memecah file wav per satu detik')
parser.add_argument('--dir', help="Target Direktori ")

args = parser.parse_args()
root_dir=args.dir

def doSplit(target,namafile):
    audio_ori = AudioSegment.from_file(target, "wav")
    chunk_length_ms = 1000 # pydub calculates in millisec
    potongan = make_chunks(audio_ori, chunk_length_ms) #Make chunks of one sec

    #Export all of the individual chunks as wav files))
    for iterasi, potongan in enumerate(potongan[:-1]):
        chunk_name = target[:-4]+"_"+"{0}".format(iterasi)+".wav"
        print ("exporting", chunk_name)
        potongan.export(chunk_name, format="wav")



sub_dir=[]
for folder in os.listdir(root_dir):
    if os.path.isdir(os.path.join(root_dir,folder)):
        sub_dir.append(folder)
    elif os.path.isfile(os.path.join(root_dir,folder)):
        pass

for index in range(len(sub_dir)):
    print(sub_dir[index])
    for data in os.listdir(os.path.join(root_dir,sub_dir[index])):
        buffer=os.path.join(root_dir,sub_dir[index])
        if os.path.isfile(os.path.join(buffer,data)):
            doSplit(os.path.join(buffer,data),data)
