import math
import os

keywords = open("keywords.txt", "r", encoding="utf8").readlines()
word_index = {keywords[index][:-1]: index for index in range(len(keywords))}

directory = "ProblemKeywords"
tf_vector = [[0 for i in range(len(keywords))] for j in range(1020)]
counter = 0

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    doc_number = 0
    for ch in f:
        if '0' <= ch <= '9':
            doc_number = 10*doc_number + int(ch)

    if os.path.isfile(f):
        file = open(f, "r", encoding="utf8")
        total = 0
        for line in file.readlines():
            if line[:-1] in word_index:
                index = word_index[line[:-1]]
                tf_vector[doc_number][index] += 1
                total += 1

        for index in range(len(keywords)):
            if total > 0:
                tf_vector[doc_number][index] /= total
        file.close()
    counter += 1


idf_vector = [0] * len(keywords)
for doc in range(counter):
    for index in range(len(keywords)):
        if tf_vector[doc][index] > 0:
            idf_vector[index] += 1


with open("idf_vector.txt", "a", encoding="utf8") as f:
    for index in range(len(keywords)):
        x = 0
        if idf_vector[index] > 0:
            x = math.log10(counter / idf_vector[index])
        f.write(str(x) + '\n')

for index in range(counter):
    doc = open("TFIDF/tfidf_{}.txt".format(index), "w", encoding="utf8")
    for i in range(len(keywords)):
        x = 0
        if idf_vector[index] > 0:
            x = tf_vector[index][i] * math.log10(counter / idf_vector[index])
        doc.write(str(x) + '\n')
    doc.close()
