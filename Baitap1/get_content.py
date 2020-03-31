'''
module: get_content
'''

import os
import string
from newspaper import Article
from nltk import sent_tokenize

# url = "https://vnexpress.net/giao-duc/nhung-tinh-huong-bi-hai-khi-hoc-tu-xa-4077359.html"

# hàm lấy nội dung từ link bài báo và trả về thể loại 
# và nội dung đã được định dạng lại 
def get_text(url):
    article = Article(url)
    article.download()
    article.parse()
    
    sentences = sent_tokenize(article.text)
    sents = []
    for sent in sentences:
        if sent is sentences[len(sentences) - 1]:
            if "..." in sent:
                sent = sent.replace("...", ".")
                sent = sent_tokenize(sent)
                for s in sent:
                    sents.append(s)
        elif '\n\n' in sent:
            sent = sent.split('\n\n')
            for s in sent:
                sents.append(s.strip())
        else:
            sents.append(sent)
    
    sentences = sents
    article_type = url.split('/')[3]
    # article_type.split('-').join(' ').capitalize()

    return sentences, article_type

# def save_to_file(file_path, sentences, url, file_wav):
#     f = open(file_path, 'w', encoding='utf-8')
    
#     f.write(url + '\n')

#     for sentence in sentences:
#         if sentence not in string.whitespace:
#             f.write(sentence + '\n')

#     f.close()

# sentences, article_type = get_text(url)
# print(sentences)

# if __name__ == '__main__':
#     # print(sentences)
#     file_path = "Data/" + article_type

#     if not os.path.exists(file_path):
#         os.makedirs(file_path, exist_ok=True)

#     file_path += "/data.txt"
#     save_to_file(file_path, sentences)

# print(sentences)