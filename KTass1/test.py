import multiprocessing


# Put "fileName" into a set
def readAsSet(fileName):
    with open(fileName, 'r') as f:
        dictList = []
        for line in f.readlines():
            dictTemp = line.strip('\n')
            dictList.append(dictTemp)
    return set(dictList)


def readAsList(fileName):
    with open(fileName, 'r') as f:
        dictList = []
        for line in f.readlines():
            dictTemp = line.strip('\n')
            dictList.append(dictTemp)
    return dictList


dictionarySet = readAsSet("dict.txt")
dictionaryList = readAsList("dict.txt")
wikiMisspell = readAsList("wiki_misspell.txt")
wikiCorrect = readAsList("wiki_correct.txt")
birkbeckMisspell = readAsList("birkbeck_misspell.txt")
birkbeckCorrect = readAsList("birkbeck_correct.txt")
testDictSet = readAsSet("test_dict.txt")
testDictList = readAsList("test_dict.txt")
testMisspell = readAsList("test_misspell.txt")
testCorrect = readAsList("test_correct.txt")


def soundexTransfer(word):
    wordSoundex = []
    temp = list(word[0])
    for letter in word[1:]:
        if letter in {'c', 'g', 'j', 'k', 'q', 's', 'x', 'z'}:
            temp.append('2')
        elif letter in {'b', 'p', 'f', 'v'}:
            temp.append('1')
        elif letter in {'d', 't'}:
            temp.append('3')
        elif letter == 'l':
            temp.append('4')
        elif letter in {'m', 'n'}:
            temp.append('5')
        elif letter == 'r':
            temp.append('6')
        else:
            pass  # Letter is in 'a e h i o u w y' or others
    deduplication = list(set(temp))
    deduplication.sort(key=temp.index)
    if len(deduplication) < 4:
        for _ in range(4 - len(deduplication)):
            deduplication.append('0')
    else:
        deduplication = deduplication[:4]
    wordSoundex.append("".join(deduplication))
    return (word, wordSoundex)

def evaluate(matchList, correctList):
    def accuracy():
        correct = 0
        seq = 0
        for matchElement in matchList:
            seq += 1
            for matchWord in matchElement:
                if matchWord in correctList[seq - 1]:
                    correct += 1
                    break
        print("The accuracy of this method is: " + str(correct / len(correctList)))

    def precision():
        correct = 0
        seq = -1
        total = 0
        for matchElement in matchList:
            seq += 1
            matchElement = list(set(matchElement))
            total += len(matchElement)
            if correctList[seq] in matchElement:
                correct += 1
                continue
        print("The precision of this method is: " + str(correct / total))

    def recall():
        correct = 0
        seq = -1
        for matchElement in matchList:
            seq += 1
            if correctList[seq] in matchElement:
                correct += 1
                continue
        print("The recall of this method is: " + str(correct / len(correctList)))

    precision()
    recall()


#if __name__ == '__main__':
    #with multiprocessing.Pool(8) as p:
       # matchList = p.map(neighbourhood, testMisspell)
    #evaluate(matchList, testCorrect)

print(soundexTransfer('aeebbeccedded'))
