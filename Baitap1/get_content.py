import os
import string
from newspaper import Article
from nltk import sent_tokenize

url = "https://vnexpress.net/thoi-su/them-3-nguoi-nhiem-ncov-tu-buddha-bar-amp-grill-4075317.html"

def get_text(url):
    article = Article(url)
    article.download()
    article.parse()
    
    sentences = sent_tokenize(article.text)
    
    article_type = url.split('/')[3]
    # article_type.split('-').join(' ').capitalize()

    return sentences, article_type

def save_to_file(file_path, sentences):
    f = open(file_path, 'w', encoding='utf-8')
    
    for sentence in sentences:
        if sentence not in string.whitespace:
            f.write(sentence + '\n')

    f.close()

sentences, article_type = get_text(url)

if __name__ == '__main__':
    print(sentences)
    file_path = "Data/" + article_type

    if not os.path.exists(file_path):
        os.makedirs(file_path, exist_ok=True)

    file_path += "/data.txt"
    save_to_file(file_path, sentences)
