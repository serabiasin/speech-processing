import tensorflow as tf
import numpy as np
import os
import json


from sklearn.preprocessing import LabelEncoder


class MFCCFeature(object):
    def __init__(self, direktoriWav=None, dirSavedFeature=None, enableGPU=True):
        self.__direktoriWav = []
        # scan direktori wav yang terdiri dari train,validasi,test
        for folder in os.listdir(direktoriWav):
            if os.path.isdir(os.path.join(direktoriWav, folder)):
                self.__direktoriWav.append(os.path.join(direktoriWav, folder))
            elif os.path.isfile(os.path.join(direktoriWav, folder)):
                pass
        print(self.__direktoriWav)
        self.__dirSaved = dirSavedFeature
        self.__enableGPU = enableGPU
        self.__jumlahKelas = 0

    def mfccExtractGPU(self, signal, sample_rate=16000, num_filters=40, low_freq=0, high_freq=None, frame_length=0.025, frame_stride=0.01, num_cepstral=32, fft_length=1024):
        #     with tf.device("/gpu:0"):
        if high_freq is None:
            high_freq = int(sample_rate / 2)

        waveform = tf.reshape(signal, [1, -1])

        # convert milisecond to frame sample signal
        frame_length = np.multiply(frame_length, sample_rate).astype('int32')
        frame_stride = np.multiply(frame_stride, sample_rate).astype('int32')

        # do Short Time Fourier Transform
        # pad_end, jika panjang sebuah spectrum tidak sama,akan dipukul rata panjangnya dan di isi dengan nilai magnitude 0
        stft = tf.signal.stft(waveform, frame_length,
                              frame_stride, fft_length=fft_length, pad_end=True)

        # convert complex number to absolute value
        spectrograms = tf.abs(stft)

        # get mel-scale
        # get number spectrogram frame
        num_spectrogram_bins = stft.shape[-1]

        # get filterbank
        linear_to_mel_weight_matrix = tf.signal.linear_to_mel_weight_matrix(
            num_filters, num_spectrogram_bins, sample_rate, low_freq,
            high_freq)

        # convert to mel-spectrogram
        mel_spectrograms = tf.tensordot(
            spectrograms, linear_to_mel_weight_matrix, 1)

        mel_spectrograms.set_shape(spectrograms.shape[:-1].concatenate(
            linear_to_mel_weight_matrix.shape[-1:]))

        # Compute a stabilized log to get log-magnitude mel-scale spectrograms.
        # dynamic range compression
        log_mel_spectrograms = tf.math.log(mel_spectrograms + 1e-6)

        # MFCC
        mfccs = tf.signal.mfccs_from_log_mel_spectrograms(
            log_mel_spectrograms)[..., :num_cepstral]
        return mfccs.numpy()[0]

    def load_file(self, path_file):
        #    with tf.device('/cpu:0'):
        audio_raw = tf.io.read_file(path_file)
        waveform, fs = tf.audio.decode_wav(audio_raw, desired_channels=1,
                                           desired_samples=-1)
        return waveform, fs

    def doExtract(self):

        self.sub_dir = []

        for indexroot in range(0, 1):
            for folder in os.listdir(self.__direktoriWav[indexroot]):
                if os.path.isdir(os.path.join(self.__direktoriWav[indexroot], folder)):
                    self.sub_dir.append(folder)
                elif os.path.isfile(os.path.join(self.__direktoriWav[indexroot], folder)):
                    pass
        print(self.sub_dir)

        # sub_dir = kelas1 dst..
        # direktori wav = trainset,valset,testset

        for root_in in range(len(self.__direktoriWav)):
            self.X = []
            self.Y = []

            for index in range(len(self.sub_dir)):
                folder = os.path.join(
                    self.__direktoriWav[root_in], self.sub_dir[index])
                print(folder)
                for wavFile in os.listdir(folder):
                    fullDirWav = os.path.join(folder, wavFile)
#           print(fullDirWav)
                    if self.__enableGPU is True:
                        with tf.device("/gpu:0"):
                            with tf.device("/cpu:0"):
                                signal, sampling = self.load_file(fullDirWav)
                                # extraction feature
                            mfcc = self.mfccExtractGPU(signal)
                            self.X.append(mfcc)
                            self.Y.append(self.sub_dir[index])
                    else:
                        with tf.device("/cpu:0"):
                            signal, sampling = self.load_file(fullDirWav)
                            # extraction feature
                            mfcc = self.mfccExtractGPU(signal)

            self.__YFilename = self.__direktoriWav[root_in]
            self.convertToNumpyFile()

        self.createJSON()

        return True

    def knownUser(self):
        self.pengguna = self.sub_dir[:3]

    def createJSON(self):
        self.countClass()
        # bikin id unik buat pencocokan nama kelas
        encoder = LabelEncoder()
        buffer = self.sub_dir[:3]
        encoder.fit(buffer)
        buffer = encoder.transform(buffer)
        label_index = np.load(self.__dirSaved + '/Y_Train.npy')

        buffer0 = (np.where(label_index == int(buffer[0])))
        buffer1 = (np.where(label_index == int(buffer[1])))
        buffer2 = (np.where(label_index == int(buffer[2])))

        index_max0 = int(np.max(buffer0))
        index_max1 = int(np.max(buffer1))
        index_max2 = int(np.max(buffer2))

        index_min0 = int(np.min(buffer0))
        index_min1 = int(np.min(buffer1))
        index_min2 = int(np.min(buffer2))

        jsonFormat = {
            "jumlah_kelas": self.jumlahKelas,
            "anggota_terdaftar": [

                {
                    'id_encoder': int(buffer[0]),
                    'nama':self.sub_dir[0],
                    'index_start':index_min0,
                    'index_end':index_max0

                },
                {
                    'id_encoder': int(buffer[1]),
                    'nama':self.sub_dir[1],
                    'index_start':index_min1,
                    'index_end':index_max1

                },
                {
                    'id_encoder': int(buffer[2]),
                    'nama':self.sub_dir[2],
                    'index_start':index_min2,
                    'index_end':index_max2
                }
            ]}
        with open(os.path.join(self.__dirSaved, 'datasetData.json'), 'w') as outfile:
            json.dump(jsonFormat, outfile)

        print("Json Created")

    def countClass(self):
        buffer = np.load(self.__YFilename)
        self.jumlahKelas = int(np.amax(buffer)) + 1

    def convertToNumpyFile(self):
        self.YBuffer = np.asarray(self.Y)
        self.XBuffer = np.asarray(self.X)
        encoder = LabelEncoder()
        encoder.fit(self.YBuffer)
        self.YBuffer = encoder.transform(self.YBuffer)

        self.__XFilename = self.__dirSaved + 'X_' + \
            os.path.basename(self.__YFilename) + '.npy'
        self.__YFilename = self.__dirSaved + 'Y_' + \
            os.path.basename(self.__YFilename) + '.npy'

        np.save(self.__XFilename, self.XBuffer)
        np.save(self.__YFilename, self.YBuffer)
        print("Saved", self.__XFilename)
        print("Saved", self.__YFilename)
