'''
Recording bằng cmd, khi chạy chương trình:
- dùng ctr+c để dừng ghi âm
- bấm enter để kết thúc bài
- bấm r để ghi âm lại đoạn vừa nói
'''

import os
import keyboard
import string
import get_content
import recording

# link bài báo
url = "https://vnexpress.net/so-hoa/netflix-giam-luu-luong-tai-viet-nam-4078017.html" 

# lấy nội dung, thể loại của bài báo
sentences, article_type = get_content.get_text(url)

print (len(sentences))

file_path = "Data/" + article_type

if not os.path.exists(file_path):
    os.makedirs(file_path, exist_ok=True)

# lưu theo format vào file data
file_path += "/"
f = open(file_path + "data.txt", 'w', encoding='utf-8')
f.write(url + '\n')

i = 0
for sent in sentences:
    if sent.isspace():
        continue 

    wav_file = "out" + str(i) + ".wav"

    # lưu tên file ghi âm, câu ghi âm vào file data
    f.write(wav_file + '\n')
    f.write(sent + '\n')

    isRepeat = True
    isExit = False
    while isRepeat:
        print('='*80)
        print(sent + '\n')
        print("Press Ctrl+C to stop the recording")
        
        recording.record_to_file(file_path + wav_file)
        
        print("Result written to " + wav_file)
        print('='*80)

        print("Press ENTER to exit, SPACE to continue, R to repeat")

        # đợi lệnh từ bàn phím
        while True:
            try:
                if keyboard.is_pressed('r'):
                    isRepeat = True
                    break
                elif keyboard.is_pressed('space'):
                    isRepeat = False
                    break
                elif keyboard.is_pressed('enter'):
                    isExit = True
                    isRepeat = False
                    break
            except:
                break
                    
    i += 1
    
    if isExit == True:
        break

print("You haven speech a article! :))")
