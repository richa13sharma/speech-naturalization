#from __future__ import division
import nltk
import pickle
from numpy.random import choice
import numpy as np
# Hello today is a lovely day to go outside to the park and have a picnic
bigram_p = {}

START_SYM = "<s>"
PERCENTAGE = 0.095
DTYPE_ERROR = "Dytpe does not exist."

def createDist(possible, dtype="uniform"):
    if(dtype=="uniform"):
        dist = []
        for i in range(len(possible)):
            dist.append(1.0/len(possible))

        return dist

    if(dtype=="right_skewed"):
        total = 0
        for it in possible:
            total += it[1]
        dist = []
        for i in range(len(possible)):
            dist.append(possible[i][1]/total)

        return dist

    else:
        return DTYPE_ERROR

def bigramSort(listOfBigrams):
    return sorted(listOfBigrams, key=lambda x: x[1], reverse=True)

def createListOfBigrams():
    f = open("./data/annotated.txt", "r")
    corpus = f.readlines()

    for sentence in corpus:
        tokens = sentence.split()
        tokens = [START_SYM] + tokens 
        bigrams = (tuple(nltk.bigrams(tokens)))
        for bigram in bigrams:
            if(bigram[0]=="(pause)" or bigram[1]=="(pause)" or \
                bigram[0]=="(uh)" or bigram[1]=="(uh)" or \
                bigram[0]=="(um)" or bigram[1]=="(um)"):
                if bigram not in bigram_p:
                    bigram_p[bigram] = 1
                else:
                    bigram_p[bigram] += 1

    listOfBigrams = [(k, v) for k, v in bigram_p.items()]
    return bigramSort(listOfBigrams)
    

def possibleAlt(sentence, listOfBigrams):
    sentence = sentence.lower()
    tokens = sentence.split()
    # tokens = [START_SYM] + tokens
    possibleBigrams = []
    for token in tokens:
        for j in range(len(listOfBigrams)):
            # FIXME: could be an 'in', clean RHS string 
            if( (token == listOfBigrams[j][0][0]) or (token == listOfBigrams[j][0][1]) ):
                possibleBigrams.append(listOfBigrams[j])
    return bigramSort(possibleBigrams)

def searchDraw(word, draw):
    for it in draw:
        if( (it[0][1] == word) or (it[0][0] == word) ):
            return 1 
    return 0

def returnDraw(word, draw):
    for it in draw:
        if( (it[0][1] == word) or (it[0][0] == word) ):
            return it[0]

def cleanInput(sent):
    sent = sent.lower()
    return sent.replace(".", "") \
                .replace(",", "") \
                .replace("\"", "")

def bigramDriver(inputSentence):
    inputSentence = cleanInput(inputSentence)
    infile = open('./obj/bigram', 'rb')
    bigrams = pickle.load(infile)
    infile.close()

    choices = np.array(possibleAlt(inputSentence, bigrams))


    # Number of choices

    print(choices)
    percentage = int(PERCENTAGE*(inputSentence.count(" ")+1))
    draw = choices[choice(choices.shape[0], percentage, p=createDist(choices))]
    print(draw)

    outputSentence = []
    for word in list(inputSentence.split()):
        if(searchDraw(word, draw)==1):
            tup = returnDraw(word, draw)
            outputSentence.append(tup[0])
            outputSentence.append(tup[1])
        else:
            outputSentence.append(word)
            # print(outputSentence)

    return ' '.join(word for word in outputSentence)

if __name__ == "__main__":
    inputSentence = cleanInput(input())
    print(bigramDriver(inputSentence))