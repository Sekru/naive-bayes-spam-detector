import re
from functools import reduce

trainingData = [
    {"message": "Interesujacy profil !!! Wiktoria . Jesli chcesz dotrzec do jeszcze wiekszej ilosci osob zapraszamy do wspolpracy www.instapromowanie.pl", "label": "spam"},
    {"message": "Piekny profil zapraszam do mnie w wolnej chwili", "label": "spam"},
    {"message": "Jak bede kupowac droższa palete do konturowania to na pewno bedzie to smashbox", "label": "ham"},
    {"message": "Mnie sie lepiej sprawdzila seria rożana, ale te też daja rade", "label": "ham"},
    {"message": "Ooo mialam w reku ten krem , ciekawe jak sie sprawdzi", "label": "ham"},
    {"message": "Jest super zapraszam także do mnie", "label": "spam"},
    {"message": "great post!", "label": "spam"},
    {"message": "Hmm zaintrygowalas mnie, koniecznie musze wyprobowac ", "label": "ham"},
    {"message": "Sprzedam takie kalendarze wiecej info na priv", "label": "spam"},
    {"message": "swietny profil i zdjecia uczieszylabym sie jeżeli bys tez zajrzala na moj profi", "label": "spam"},
    {"message": "Wow, wyglada pieknie. Chyba czas odlożyc troche pieniedzy", "label": "ham"},
    {"message": "Kochana super profil!! W wolnej chwili zapraszam do siebie", "label": "spam"},
    {"message": "Oj tak mam ich mnostwo", "label": "ham"},
    {"message": "I like for my art? Follow me!", "label": "spam"},
    {"message": "Super by bylo gdyby kazdy nie byl otwarty i wymacany kiedy producenci znajda na to myk", "label": "ham"},
    {"message": "kupilam te same pedzle rownież z mysla że do rozswietlacza bedzie jak znalazl do bronzera", "label": "ham"},
    {"message": "Ja też upolowalam pedzle z biedry mam ten do pudru, rożu i rozswietlacza", "label": "ham"},
    {"message": "Dopiero wczoraj udalo mi sie je kupic w naturze ciagle na polkach byly braki", "label": "ham"},
    {"message": "Kupilam wczoraj krem z tej serii z Bielenda i jestem zachwycona", "label": "ham"},
    {"message": "super profil w wolnej chwili zapraszam do mnie", "label": "spam"},
    {"message": "Piekny profil zapraszam do mnie w wolnej chwili", "label": "spam"},
]

def countWords(counter, words):
    for word in words:
        counter[word] = counter.get(word, 0) + 1

def preprocess_string(words):
    cleaned = re.sub('[^a-z\s]+', ' ', words,flags=re.IGNORECASE)
    cleaned = re.sub(r'\b\w{1,3}\b', '', cleaned)
    cleaned = re.sub('(\s+)', ' ', cleaned)
    cleaned = cleaned.lower()
    
    return cleaned.split(' ')

def train(trainingData):
    spamWords = {}
    hamWords = {}
    totalSpam = 0
    totalHam = 0
    for s in range(len(trainingData)):
        if trainingData[s]["label"] == "spam":
            totalSpam = totalSpam + 1
            spamWordsArray = preprocess_string(trainingData[s]["message"])
            countWords(spamWords, spamWordsArray)

        if trainingData[s]["label"] == "ham":
            totalHam = totalHam + 1
            hamWordsArray = preprocess_string(trainingData[s]["message"])
            countWords(hamWords, hamWordsArray)

    return spamWords, hamWords, totalSpam, totalHam

def think(wordsString, pSpam, pHam, spamWords, hamWords):
    pSpam = totalSpam / totalCounter
    pHam = totalHam / totalCounter
    pSWords = []
    pHWords = []
    processedWords = preprocess_string(wordsString)
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

    pSResult = reduce(lambda x, y: x * y, pSWords)
    pHResult = reduce(lambda x, y: x * y, pHWords)

    if (pSResult > pHResult):
        print("Spam")
    if (pSResult < pHResult):
        print("Ham")
    if (pSResult == pHResult):
        print("Hard to say...")
    
if __name__ == "__main__":
    spamWords, hamWords, totalSpam, totalHam = train(trainingData)
    totalCounter = len(trainingData)
    while True:
        something = input("Please enter something: ")
        think(something, totalSpam, totalHam, spamWords, hamWords)
