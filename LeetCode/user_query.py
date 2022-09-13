import os.path
import re
import sys
import json
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

query_string = sys.argv[1][1:-1]
# query_string = "zigzag-conversion"
directory = "/Users/vinay/PycharmProjects/DSA_SearchEngine/BackEnd/LeetCode"

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


keywords = open(directory + "/keywords.txt", "r", encoding="utf8").readlines()
word_index = {keywords[index][:-1]: index for index in range(len(keywords))}
query_keywords = preprocess(query_string)
# print(query_keywords)

tfidf_query = [0] * len(keywords)
for word in query_keywords:
    if word in word_index:
        tfidf_query[word_index[word]] += 1


with open(directory + "/idf_vector.txt", "r", encoding="utf8") as f:
    values = f.readlines()
    for index in range(len(keywords)):
        tfidf_query[index] *= float(values[index]) / len(query_keywords)


directory += "/TFIDF/"
similarity_scores = []

for filename in os.listdir(directory):
    f = directory + filename
    doc = open(f, "r", encoding="utf8")
    lines = doc.readlines()
    doc_number = 0

    for ch in filename:
        if '0' <= ch <= '9':
            doc_number = 10*doc_number + int(ch)
    
    similarity = 0
    for i in range(len(lines)):
        similarity += float(lines[i][:-1]) * tfidf_query[i]
    similarity_scores.append((similarity, doc_number))
    doc.close()


similarity_scores.sort(reverse=True)
urls = open(directory[:-7] + "/urls.txt", "r", encoding="utf8").readlines()
results = []
# print(similarity_scores[:5])

for i in range(5):
    index = similarity_scores[i][1]
    results.append(urls[index][:-1])

# print(results)
print(json.dumps(results))
