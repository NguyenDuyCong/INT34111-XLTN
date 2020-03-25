import os
from nltk.tokenize import sent_tokenize

folder_path = 'Data'

dirs = os.listdir(folder_path)
for path in dirs:
    files = os.listdir(path)
    for file_name in files:
        with open(os.path.join(folder_path, path, file_name), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines = ' '.join(lines)
        lines = sent_tokenize(lines)

        out_file = file_name + '_out.txt'
        with open(os.path.join(folder_path, path, out_file), 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
        