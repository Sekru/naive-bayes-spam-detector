import re
from functools import reduce
import csv
import time
import json

def countWords(counter, words):
    for word in words:
        if word != "subject":
            counter[word] = counter.get(word, 0) + 1

def preprocess_string(words):
    cleaned = re.sub('[^a-z\s]+', ' ', words,flags=re.IGNORECASE)
    cleaned = re.sub(r'\b\w{1,3}\b', '', cleaned)
    cleaned = cleaned.lower()
    cleaned = re.sub('(\s+)', ' ', cleaned)
    return cleaned.split(' ')

def extractType(wordsString):
    try:
        return wordsString[1]
    except TypeError:
        pass

def train():
    trainingData = []
    with open('./static/emails.csv', newline='') as csvfile:
        trainingData = list(csv.reader(csvfile))
    spamWords = {}
    hamWords = {}
    totalSpam = 0
    totalHam = 0
    start = time.time()
    end = time.time()
    for s in range(len(trainingData)):
        category = extractType(trainingData[s])

        if category == '1':
            totalSpam = totalSpam + 1
            spamWordsArray = preprocess_string(trainingData[s][0])
            countWords(spamWords, spamWordsArray)

        if category == '0':
            totalHam = totalHam + 1
            hamWordsArray = preprocess_string(trainingData[s][0])
            countWords(hamWords, hamWordsArray)
    fh = open('./static/hamWords.json','w')
    fh.write(json.dumps(hamWords))
    fh.close()
    fs = open('./static/spamWords.json','w')
    fs.write(json.dumps(spamWords))
    fs.close()
    fs = open('./static/generals.json','w')
    fs.write(json.dumps({"totalSpam": totalSpam, "totalHam": totalHam, "total": totalSpam + totalHam}))
    fs.close()
    end = time.time()
    print(str(end - start) + "sec")
    return str(end - start)

def openResults():
    with open('./static/generals.json', 'r') as g:
        generals = json.load(g)
        totalCounter = generals['total']
        totalSpam = generals['totalSpam']
        totalHam = generals['totalHam']
    with open('./static/spamWords.json', 'r') as s:
        spamWords = json.load(s)
    with open('./static/hamWords.json', 'r') as h:
        hamWords = json.load(h)

    return totalCounter, totalSpam, totalHam, spamWords, hamWords

def think(wordsString):
    totalCounter, totalSpam, totalHam, spamWords, hamWords = openResults()
    pSpam = totalSpam / totalCounter
    pHam = totalHam / totalCounter
    pSWords = []
    pHWords = []
    processedWords = preprocess_string(wordsString['data'])
    for word in processedWords:
        pSW = 0
        pHW = 0
        try:
            spamWord = spamWords[word]
        except KeyError:
            spamWord = 0

        try:
            hamWord = hamWords[word]
        except KeyError:
            hamWord = 0

        try:
            pSW = ((spamWord/totalSpam) * pSpam) / (((spamWord/totalSpam) * pSpam) + ((hamWord/totalHam) * pHam))
            pHW = ((hamWord/totalHam) * pHam) / (((hamWord/totalHam) * pHam) + ((spamWord/totalSpam) * pSpam))
        except ZeroDivisionError:
            pass

        pSWords.append(pSW)
        pHWords.append(pHW)

    pSResult = reduce(lambda x, y: x + y, pSWords) / len(pSWords)
    pHResult = reduce(lambda x, y: x + y, pHWords) / len(pHWords)
    return pSResult, pHResult