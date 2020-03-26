'''
Recording bằng cmd, khi chạy chương trình:
- dùng ctr+c để dừng ghi âm
- bấm enter để kết thúc bài
'''

import pyaudio
import wave
import keyboard
import time

from nltk import sent_tokenize
from get_content import article_type

chunk = 1024
sample_format = pyaudio.paInt16
channels = 2 
fs = 44100

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

def record_to_file(file_path):
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    sample_width, frames = record()
    wf.setsampwidth(sample_width)
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == '__main__':
    file_path = 'Data/' + article_type + '/'
    f = open(file_path + 'data.txt', 'r', encoding='utf-8')

    lines = f.readlines()
    lines = ' '.join(lines)
    sentences = sent_tokenize(lines) 

    i = 0
    for sent in sentences:
        print('='*80)
        print(sent + '\n')
        print("Press Ctrl+C to stop the recording")

        record_to_file(file_path + 'out'+ str(i) +'.wav')

        print("Result written to out" + str(i) + ".wav")
        
        i += 1

        print('='*80)

        print("Press ENTER if you want to exit recording.")
        # time.sleep(5)
        isExit = False
        while True:
            try:
                if keyboard.is_pressed('Enter'):
                    isExit = True
                    break
            except:
                break
        
        if isExit == True:
            break


    print("You haven speech a article! :))")
   