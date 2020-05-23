import tkinter
import tkinter.messagebox
import pyaudio
import wave
import os
import librosa
import numpy as np
import math
import pickle


class Recoder:

    def __init__(self, chunk=1024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):

        # thiết lập các thông số cơ bản
        self.main = tkinter.Tk()
        self.collections = []
        self.main.geometry('500x300')
        self.main.title('Record')
        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        self.st = 1
 
        # frame
        self.buttons = tkinter.Frame(self.main, padx=100)

        # đóng gói frame để hiển thị được
        self.buttons.pack(fill=tkinter.BOTH)


        # Start and Stop buttons
        self.strt_rec = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Start Recording', command=lambda: self.start_record())
        self.strt_rec.grid(row=0, column=0)
        self.stop_rec = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text='Stop Recording', command=lambda: self.stop_record())
        self.stop_rec.grid(row=0, column=1, padx=5, pady=5)
        self.detect = tkinter.Button(self.buttons, width=10, padx=10, pady=5, text="Predict", command=lambda: self.predict_voice())
        self.detect.grid(row=0, column=2)

        # lable 
        self.predict_lbl = tkinter.Label(self.main, text="PREDICT")
        self.predict_lbl.pack(pady=10)
        tkinter.mainloop()

    def start_record(self):
        self.st = 1
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        while self.st == 1:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            print("recoding...")
            self.main.update()

        stream.close()

        # lưu file test
        wf = wave.open('test.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def stop_record(self):
        self.st = 0
        print("stopping")

    def get_mfcc(self, file_path="test.wav"):
        y, sr = librosa.load(file_path) # read .wav file
        hop_length = math.floor(sr*0.010) # 10ms hop
        win_length = math.floor(sr*0.025) # 25ms frame
        # mfcc is 12 x T matrix
        mfcc = librosa.feature.mfcc(
            y, sr, n_mfcc=12, n_fft=1024,
            hop_length=hop_length, win_length=win_length)
        # substract mean from mfcc --> normalize mfcc
        mfcc = mfcc - np.mean(mfcc, axis=1).reshape((-1,1)) 
        # energy feature
        rms = librosa.feature.rms(y, hop_length=hop_length)
        frame_feature = np.concatenate([mfcc, rms], axis=0)
        # delta feature 1st order and 2nd order
        delta1 = librosa.feature.delta(frame_feature, order=1, mode='nearest')
        delta2 = librosa.feature.delta(frame_feature, order=2, mode='nearest')
        # X is 39 x T
        X = np.concatenate([frame_feature, delta1, delta2], axis=0) # O^r
        # return T x 39 (transpose of X)
        return X.T # hmmlearn use T x N matrix

    def predict_voice(self):
        with open("gmm_hmm1.pkl", "rb") as file:
            self.models = pickle.load(file)

        O = self.get_mfcc()
        score = {cname: model.score(O, [len(O)]) for cname, model in self.models.items()}
        inverse = [(value, key) for key, value in score.items()]
        self.predict = max(inverse)[1]

        text = "predict: " + self.get_text(self.predict)
        self.predict_lbl.config(text=text)
        print(self.predict)

    def get_text(self, predict):
        if predict == "hai":
            return "hai"
        if predict == "tien":
            return "tiền"
        if predict == "duong":
            return "đường"
        if predict == "y_te":
            return "y tế"
        if predict == "benh_nhan":
            return "bệnh nhân"

record = Recoder()