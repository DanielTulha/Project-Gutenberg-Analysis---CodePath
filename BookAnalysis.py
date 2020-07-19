from heapq import *
import collections
import random

bookName = "A Tale Of Two Cities - Charles Dickens.txt"
mostCommonWordsFile = "1000mostCommonWords.txt"

def getWordList(fileName):
    file = open(fileName, 'rt', encoding='utf-8')
    text = file.read()
    file.close()

    words = text.split()
    return words

def getTotalNumberOfWords(fileName):

    wordList = getWordList(fileName)
    return len(wordList)

def getTotalUniqueWords(fileName):

    words = getWordList(fileName)
    uniqueWords = set(words)
    return len(uniqueWords)

def getMostCommonWordsInEnglish(numberOfWords):
    commonWordList = getWordList(mostCommonWordsFile)
    return commonWordList[:numberOfWords]

def getMostFrequentWords(fileName, numberOfWords, wordFilter = set()):

    wordCount = collections.defaultdict(int)

    class Word:
        def __init__(self, word):
            self.word = word

        def getWord(self):
            return self.word

        def __lt__(self, other):
            return wordCount[self.word] < wordCount[other.getWord()]

    wordList = getWordList(fileName)

    mostCommonWords = []
    wordSet = set()

    for word in wordList:
        if word in wordFilter or word.lower() in wordFilter:
            continue

        wordCount[word] += 1

        if word in wordSet:
            heapify(mostCommonWords)
            continue

        if len(mostCommonWords) < numberOfWords:
            newWord = Word(word)
            heappush(mostCommonWords, newWord)
            wordSet.add(word)

        elif wordCount[word] > wordCount[mostCommonWords[0].getWord()]:
            newWord = Word(word)
            removed = heapreplace(mostCommonWords, newWord)
            wordSet.remove(removed.getWord())
            wordSet.add(word)

    frequentWordsDescending = collections.deque([])
    while mostCommonWords:
        w = heappop(mostCommonWords).getWord()
        frequentWordsDescending.appendleft([w, wordCount[w]])

    return list(frequentWordsDescending)


def getMostInterestingFrequentWords(fileName, numberOfWords, numberOfFilteredWords):
    commonWordsSet = set(getMostCommonWordsInEnglish(numberOfFilteredWords))
    return getMostFrequentWords(fileName, numberOfWords, commonWordsSet)

def getLeastFrequentWords(fileName, numberOfWords):

    wordCount = collections.defaultdict(int)

    class Word:
        def __init__(self, word):
            self.word = word

        def getWord(self):
            return self.word

        def __lt__(self, other): # Max heap comparator
            return wordCount[self.word] > wordCount[other.getWord()]

    wordList = getWordList(fileName)

    leastCommonWords = []
    wordSet = set()

    for word in wordList:
        wordCount[word] += 1

        if word in wordSet:
            heapify(leastCommonWords)
            continue

        if len(leastCommonWords) < numberOfWords:
            newWord = Word(word)
            heappush(leastCommonWords, newWord)
            wordSet.add(word)

        elif wordCount[word] < wordCount[leastCommonWords[0].getWord()]:
            newWord = Word(word)
            removed = heapreplace(leastCommonWords, newWord)
            wordSet.remove(removed.getWord())
            wordSet.add(word)

    leastCommonWordsDescending = collections.deque([])
    while leastCommonWords:
        w = heappop(leastCommonWords).getWord()
        leastCommonWordsDescending.appendleft([w, wordCount[w]])
    return list(leastCommonWordsDescending)


def getFrequencyOfWord(fileName, desiredWord):
    wordList = getWordList(fileName)

    currentChapter = 0
    wordsPerChapter = []

    for word in wordList:
        if word == 'Chapter':
            wordsPerChapter.append(0)

        if word == desiredWord and wordsPerChapter:
            wordsPerChapter[-1] += 1

    return wordsPerChapter

def getChapterQuoteAppears(fileName, desiredQuote):
    wordList = getWordList(fileName)

    currentChapter = matchedWords = wordIndex = 0
    quote = desiredQuote.split()

    while wordIndex < len(wordList):
        word = wordList[wordIndex]
        if word == 'Chapter':
            currentChapter += 1

        if word == quote[matchedWords]:
            matchedWords += 1
            if matchedWords == len(quote):
                return currentChapter

        elif matchedWords > 0:
            wordIndex = wordIndex - matchedWords
            matchedWords = 0

        wordIndex += 1

    return -1


def generateSentence(fileName, sentenceLength = 20):

    wordList = getWordList(fileName)

    def generateSentenceRecursively(currentWord, currentSentence):
        currentSentence += ' ' + currentWord
        if len(currentSentence.split()) == sentenceLength:
            return currentSentence

        wordIndexes = []

        for wordIndex in range(len(wordList)):
            if currentWord == wordList[wordIndex]:
                wordIndexes.append(wordIndex + 1)

        randomIndex = random.randrange(len(wordIndexes))
        randomWord = wordList[wordIndexes[randomIndex]]
        return generateSentenceRecursively(randomWord, currentSentence)

    return generateSentenceRecursively('The', '')


# print()
# print('A Tale Of Two Cities contains %s words' % getTotalNumberOfWords(bookName))
# print()
# print('A Tale Of Two Cities contains %s unique words' % getTotalUniqueWords(bookName))
# print()
# print('The twenty most common words in A Tale Of Two Cities are', str(getMostFrequentWords(bookName, 20)))
# print()
# print('The twenty most interesting words in A Tale Of Two Cities are', str(getMostInterestingFrequentWords(bookName, 20, 1000)))
# print()
# print('The twenty least common words in A Tale Of Two Cities are', str(getLeastFrequentWords(bookName, 20)))
# print()
# print("The frequency of 'Monsieur' by chapter is", str(getFrequencyOfWord(bookName, 'Monsieur')))
# print()
# print("The quote 'The coffee-room had no other occupant,' can be found in chapter", getChapterQuoteAppears(bookName, 'The coffee-room had no other occupant,'))
# print()
# for i in range(20):
#     print('Sample random sentence:', generateSentence(bookName))
# print()
