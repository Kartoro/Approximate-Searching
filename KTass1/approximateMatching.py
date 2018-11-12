import multiprocessing

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


# Neighbourhood Search:
def neighbourhood(word, dictionary = dictionaryList):
    def levenshtein(s1, s2):
        if abs(len(s1) - len(s2)) > 1:
            return False

        if len(s1) < len(s2):
            return levenshtein(s2, s1)
        previousRow = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            currentRow = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previousRow[j + 1] + 1
                deletions = currentRow[j] + 1
                substitutions = previousRow[j] + (c1 != c2)
                currentRow.append(min(insertions, deletions, substitutions))
            previousRow = currentRow
        if previousRow[-1] == 1:
            return True
        else:
            return False

    # for word in misspellList:
    matchList = []
    for dictWord in dictionary:
        if levenshtein(word, dictWord):
            matchList.append(dictWord)
    print(matchList)
    return matchList


# Global Edit Distance: Needleman–Wunsch Algorithm
def globalEditDistance(word, dictionary = dictionaryList):
    def needleman(s1, s2):
        if len(s1) < len(s2):
            return needleman(s2, s1)
        previousRow = range(-len(s2) - 1, 0)
        for i, c1 in enumerate(s1):
            currentRow = [-i - 1]
            for j, c2 in enumerate(s2):
                insertions = previousRow[j + 1] - 1
                deletions = currentRow[j] - 1
                if c1 != c2:
                    match = -1
                else:
                    match = 1
                substitutions = previousRow[j] + match
                currentRow.append(max(insertions, deletions, substitutions))
            previousRow = currentRow
        return previousRow[-1]

    distanceList = []
    for dictWord in dictionary:
        distance = needleman(word, dictWord)
        distanceList.append(distance)
    dictWithDistance = dict(zip(dictionary, distanceList))
    maxDistanceList = []
    maxDistance = max(dictWithDistance.values())
    for key, value in dictWithDistance.items():
        if value == maxDistance:
            maxDistanceList.append(key)
    print(word)
    return maxDistanceList


# Local Edit Distance: Smith–Waterman Algorithm
def localEditDistance(word, dictionary = dictionaryList):
    def waterman(s1, s2):
        maxDistance = 0
        if len(s1) < len(s2):
            return waterman(s2, s1)
        previousRow = [0] * (len(s2) + 1)
        for i, c1 in enumerate(s1):
            currentRow = [0]
            for j, c2 in enumerate(s2):
                substitutions = previousRow[j] + (c1 == c2)
                currentRow.append(max(0, substitutions))
                maxTemp = max(currentRow)
                if maxTemp > maxDistance:
                    maxDistance = maxTemp
            previousRow = currentRow
        return maxDistance

    distanceList = []
    for dictWord in dictionary:
        distance = waterman(word, dictWord)
        distanceList.append(distance)
    dictWithDistance = dict(zip(dictionary, distanceList))
    maxDistanceList = []
    maxDistance = max(dictWithDistance.values())
    for key, value in dictWithDistance.items():
        if value == maxDistance:
            maxDistanceList.append(key)
    return maxDistanceList


# N-Gram Distance:
def nGram(word, dictionary = dictionaryList):
    def gram(word, n=2):
        gramList = []
        wordLen = len(word)
        gramList.append(word[0])
        for i in range(wordLen - 1):
            gramList.append(word[i:i + 2])
        gramList.append(word[-1])
        return gramList

    dictWordGramList = []
    for dictWord in dictionary:
        dictWordGramList.append(gram(dictWord))
    print(word)
    distanceList = []
    wordGram = gram(word)
    for dictWordGram in dictWordGramList:
        distance = len(wordGram) + len(dictWordGram) - 2 * len(list(set(wordGram).intersection(set(dictWordGram))))
        distanceList.append(distance)
    dictWithDistance = dict(zip(dictionary, distanceList))
    minDistanceList = []
    minDistance = min(dictWithDistance.values())
    for key, value in dictWithDistance.items():
        if value == minDistance:
            minDistanceList.append(key)
    return minDistanceList


# Soundex:
def soundex(word, dictionary = dictionaryList):
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

    dictSoundexList = []
    for dictionaryWord in dictionary:
        dictSoundexList.append(soundexTransfer(dictionaryWord))
    correctListTemp = []
    wordTransfer = soundexTransfer(word)
    for sound in dictSoundexList:
        if wordTransfer[1] == sound[1]:
            correctListTemp.append(sound[0])
    return correctListTemp


def evaluate(matchList, correctList):

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


def inputFileName():
    # global misspellList, correctList, dictionary

    misspellFileName = input("Please input the misspell dictionary: ")
    if misspellFileName == "wiki":
        misspellList = wikiMisspell
    elif misspellFileName == "birk":
        misspellList = birkbeckMisspell
    else:
        misspellList = testMisspell  # *test only*
        # print("No such file. Try again.")
        # inputFileName()

    correctFileName = input("Please input the correct dictionary: ")
    if correctFileName == "wiki":
        correctList = wikiCorrect
    elif correctFileName == "birk":
        correctList = birkbeckCorrect
    else:
        correctList = testCorrect  # *test only*
        # print("No such file. Try again.")
        # inputFileName()

    dictionaryName = input("Please input the dictionary you wish to use: ")
    if dictionaryName == "dictlist":
        dictionary = dictionaryList
    elif dictionaryName == "dictset":
        dictionary = dictionarySet
    elif dictionaryName == "testset":
        dictionary = testDictSet
    elif dictionaryName == "testlist":
        dictionary = testDictList
    else:
        dictionary = dictionaryList  # *test only*
        # print("No such file. Try again.")
        # inputFileName()

    return misspellList, correctList, dictionary


def inputMethod():
    global method

    print("1 - Neighbourhood Search")
    print("2 - Global Edit Distance: Needleman–Wunsch Algorithm")
    print("3 - Local Edit Distance: Smith–Waterman Algorithm")
    print("4 - N-Gram Distance")
    print("5 - Soundex")

    methodName = input("Please input the method number you wish to use: ")
    if methodName == "1":
        method = neighbourhood
    elif methodName == "2":
        method = globalEditDistance
    elif methodName == "3":
        method = localEditDistance
    elif methodName == "4":
        method = nGram
    elif methodName == "5":
        method = soundex
    else:
        print("No such method. You should input a number from 1 to 5. Try again.")
        inputMethod()

    return method


def run():
    print("*** Approximate Matching Program ***")
    misspellList, correctList, dictionary = inputFileName()
    method = inputMethod()
    with multiprocessing.Pool(8) as p:
        matchList = p.map(method,misspellList)
    # matchList = method(misspellList, dictionary)
    evaluate(matchList, correctList)
    # ans = input("Try another method? Y/N: ")
    # if ans == "Y" or ans == "y": run()
    exit(0)


# Main
if __name__ == '__main__':

    run()
