'''
module: recording
'''

import pyaudio
import wave
import keyboard
import time

from nltk import sent_tokenize
# from get_content import article_type

chunk = 1024
sample_format = pyaudio.paInt16
channels = 2 
fs = 44100

# thực hiện quá trình ghi âm
def record():
    p = pyaudio.PyAudio()
    
    stream = p.open(format=sample_format, 
                    channels=channels, 
                    rate=fs, 
                    frames_per_buffer=chunk, 
                    input=True)
    
    print("Start recording...")

    frames = []

    try:
        while True:
            data = stream.read(chunk)
            frames.append(data)
    except KeyboardInterrupt:
        print("Done recording!")
    except Exception as e:
        print(str(e))

    sample_width = p.get_sample_size(sample_format)

    stream.stop_stream()
    stream.close()
    p.terminate()

    return sample_width, frames

# lưu bản ghi âm sang định dạng tệp .wav
def record_to_file(file_path):
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    sample_width, frames = record()
    wf.setsampwidth(sample_width)
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
   