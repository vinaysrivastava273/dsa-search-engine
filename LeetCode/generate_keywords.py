import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import os

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def preprocess(text):
    text_p = ""
    for char in text:
        if char not in string.punctuation:
            text_p += char
        else:
            text_p += ' '

    words = word_tokenize(text_p)
    filtered_words = [word for word in words if word not in stop_words]
    stemmed = [lemmatizer.lemmatize(word) for word, tag in pos_tag(filtered_words)]
    return stemmed


directory = 'Docs'
keywords = []

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    doc_number = 0
    for ch in f:
        if '0' <= ch <= '9':
            doc_number = 10*doc_number + int(ch)

    if os.path.isfile(f):
        cur = open(f, "r", encoding="utf8")
        words = preprocess(cur.read().lower())
        keywords += words
        cur.close()

        with open("ProblemKeywords/keywords_{}.txt".format(doc_number), "w", encoding="utf8") as cur:
            cur.write('\n'.join(words))


keywords = set(keywords)
with open("keywords.txt", "w", encoding="utf8") as file:
    for keyword in keywords:
        file.write(keyword + '\n')
