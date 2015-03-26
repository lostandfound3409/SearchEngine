from WebDB import WebDB
import os
from TermDictionary import TermDictionary
from stemming.porter2 import stem
from Evaluation import Evaluation
from random import shuffle


class Queries():
    itemFolder = 'data\item'
    cleanFolder = r'data\clean'
    termDict = TermDictionary()
    db = WebDB('data\cache.db')
    eval = Evaluation()

    #Generate the positional list for all words in the clean files
    print("Generating positional list...")
    for root, dirs, files in os.walk(cleanFolder):
        for file in files:
            count = 0
            log = open(os.path.join(root, file), 'r')
            docID = os.path.splitext(file)[0]
            for term in log.readlines():
                count += 1
                termDict.addWord(term, docID, count)
            log.close()

    def token_query(self):
        tokenQuery = input("Enter a single Token: ")
        tokenQuery = stem(tokenQuery).lower()
        print("Actual Search: " + tokenQuery)
        tokenId = self.termDict.getPosFromQuery(tokenQuery)
        tokenList = []
        for fileId, pos in tokenId.items():
            if (self.db.lookupCachedURL_byID(int(fileId))) is not None:
                tokenList.append(str(self.db.lookupCachedURL_byID(int(fileId))))
        self.print_results(tokenList)


    def and_query(self):
        andQuery = input("Enter 2 tokens: ")
        andQuery = andQuery.split()
        andQuery[0] = stem(andQuery[0]).lower()
        andQuery[1] = stem(andQuery[1]).lower()
        print("Actual Search: " + andQuery[0] + " " + andQuery[1])
        andList = []
        andId1 = self.termDict.getPosFromQuery(andQuery[0])
        andId2 = self.termDict.getPosFromQuery(andQuery[1])
        if andId1 is not None and andId2 is not None:
            for key1, value1 in andId1.items():
                for key2, value2 in andId2.items():
                    if key1 == key2:
                        andList.append(self.db.lookupCachedURL_byID(int(key2)))
        self.print_results(andList)

    def or_query(self):
        orQuery = input("Enter 2 tokens: ")
        orQuery = orQuery.split()
        orQuery[0] = stem(orQuery[0])
        orQuery[1] = stem(orQuery[1])
        print("Actual Search: " + orQuery[0] + " " + orQuery[1])
        orList = []
        orId1 = self.termDict.getPosFromQuery(orQuery[0])
        orId2 = self.termDict.getPosFromQuery(orQuery[1])
        if orId1 is not None and orId2 is not None:
            for key1, value1 in orId1.items():
                check = self.db.lookupCachedURL_byID(int(key1))
                if check not in orList:
                    orList.append(check)
                    for key2, value2 in orId2.items():
                        check = self.db.lookupCachedURL_byID((int(key2)))
                        if check not in orList:
                            orList.append(check)
        self.print_results(orList)

    def phrase_query(self):
        phraseQuery = input("Enter a 2 token phrase separated by a space: ")
        phraseQuery = phraseQuery.split()
        phraseQuery[0] = stem(phraseQuery[0])
        phraseQuery[1] = stem(phraseQuery[1])
        print("Actual Search: " + phraseQuery[0] + " " + phraseQuery[1])
        phraseList = []
        phraseId1 = self.termDict.getPosFromQuery(phraseQuery[0])
        phraseId2 = self.termDict.getPosFromQuery(phraseQuery[1])
        if phraseId1 is not None and phraseId2 is not None:
            try:
                for key1, value1 in phraseId1.items():
                    for key2, value2 in phraseId2.items():
                        if key1 == key2:
                            for allValues1 in value1:
                                for allValues2 in value2:
                                    if int(allValues1) - int(allValues2) == -1:
                                        listCheck = self.db.lookupCachedURL_byID(int(key1))
                                        if listCheck not in phraseList:
                                            phraseList.append(listCheck)
                                            break
            except TypeError:
                print("0 results")
        self.print_results(phraseList)

    def near_query(self):
        nearQuery = input("Enter a 2 token query: ")
        range = input("Enter a range: ")
        nearQuery = nearQuery.split()
        nearQuery[0] = stem(nearQuery[0])
        nearQuery[1] = stem(nearQuery[1])
        print("Actual Search: " + nearQuery[0] + " " + nearQuery[1])
        nearList = []
        nearId1 = self.termDict.getPosFromQuery(nearQuery[0])
        nearId2 = self.termDict.getPosFromQuery(nearQuery[1])
        if nearId1 is not None and nearId2 is not None:
            try:
                for key1, value1 in nearId1.items():
                    for key2, value2 in nearId2.items():
                        if key1 == key2:
                            for allValues1 in value1:
                                for allValues2 in value2:
                                    if int(allValues1) - int(allValues2) <= int(range) or int(allValues2) - int(
                                            allValues1) <= int(range):
                                        listCheck = self.db.lookupCachedURL_byID(int(key1))
                                        if listCheck not in nearList:
                                            nearList.append(listCheck)
                                            break
            except TypeError:
                print("0 results")
        self.print_results(nearList)

    #-------------------------------------------
    # Function for free query
    #-------------------------------------------
    def theQuery(self):
        query = input("Enter a query: ")
        query = stem(query).lower()
        docWeight = input("Document weight(nnn or ltc): ")
        self.termDict.calcWeight(docWeight)
        queryWeight = input("Query weight(nnn or ltc): ")
        scores = self.termDict.calcQuery(query, queryWeight)
        count = 0
        relevant = []
        for doc in scores:
            if count < 5 and self.db.lookupCachedURL_byID(int(doc[0])) != None:
                relevant.append(str(self.db.lookupCachedURL_byID((int(doc[0])))+ " " + str(doc[1])))
            count += 1
        self.print_results(relevant)
    #-------------------------------------------
    # Function for evaluation purposes. Uses automatic search for terms in item files.
    #-------------------------------------------
    def autoQuery(self):
        docWeighting = ["nnn","ltc"]
        queryWeighting = ["nnn","ltc"]
        print("Evaluating all documents...")
        for weight in docWeighting:
            self.termDict.calcWeight(weight)
            for weight2 in queryWeighting:
                print("Evaluating next weighting scheme...")
                meanAvgPrec = 0
                meanRPrec = 0
                meanPrec = 0
                meanAuc = 0
                for root, dirs, files in os.walk(self.itemFolder):
                    for file in files:
                        log = open(os.path.join(root, file), 'r')
                        for query in log.readlines():
                            currentList = []
                            #Grab the query and clean it up
                            query = query.replace(",", "")
                            query = stem(query).lower()
                            scores = self.termDict.calcQuery(query.strip(), weight2)
                            for doc in scores:
                                if self.db.lookupCachedURL_byID(int(doc[0])) is not None:
                                    #Grab the database search result and clean it up
                                    splitTerm = str(self.db.lookupCachedURL_byID(int(doc[0]))).split(",")
                                    splitTerm = splitTerm[1].split(":")
                                    splitTerm[0] = splitTerm[0].replace("'", "")
                                    if stem(splitTerm[0]).lower().strip() == query.strip(): #Comparing the media type of the query to the database result
                                        currentList.append(1)#Search is relevant
                                    else:
                                        currentList.append(0)#Search is non-relevant
                            meanAvgPrec += self.eval.avgPrecision(currentList)
                            meanRPrec += self.eval.rPrecision(currentList)
                            meanPrec += self.eval.precision(currentList, 10)
                            meanAuc += self.eval.areaUnderCurve(currentList)
                print(weight, " ", weight2)
                print("Mean Avg. Precision: ", meanAvgPrec / 39)
                print("Mean Precision @ R: ", meanRPrec / 39)
                print("Mean Precision @ 10: ", meanPrec / 39)
                print("Mean Area Under Curve: ", meanAuc / 39, "\n")

    # Random evaluation metrics
        shuffleList = []
        meanAvgPrec = 0
        meanRPrec = 0
        meanPrec = 0
        meanAuc = 0
        for x in range(0, 200):
            for x in range(0, 357):
                shuffleList.append(0)
            for x in range(0, 10):
                shuffleList.append(1)
            shuffle(shuffleList)
            meanAvgPrec += self.eval.avgPrecision(shuffleList)
            meanRPrec += self.eval.rPrecision(shuffleList)
            meanPrec += self.eval.precision(shuffleList, 10)
            meanAuc += self.eval.areaUnderCurve(shuffleList)

        print("Random Evaluation")
        print("Mean Avg. Precision: ", meanAvgPrec / 200)
        print("Mean Precision @ R: ", meanRPrec / 200)
        print("Mean Precision @ 10: ", meanPrec / 200)
        print("Mean Area Under Curve: ", meanAuc / 200, "\n")



    #-------------------------------------------
    # Print the results of a search
    #-------------------------------------------
    def print_results(self, listToPrint):
        itemCount = 0
        if listToPrint is not None:
            for item in listToPrint:
                if item is not None:
                    itemCount += 1
                    print(str(itemCount) + ". " + str(item))
        else:
            print("No Results")