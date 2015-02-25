from WebDB import WebDB
import os
from TermDictionary import TermDictionary
from stemming.porter2 import stem

class Queries():
    itemFolder = 'data\item'
    cleanFolder = r'data\clean'
    termDict = TermDictionary()
    db = WebDB('data\cache.db')

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
        tokenList =[]
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
                                    if int(allValues1) - int(allValues2) <= int(range) or int(allValues2) - int(allValues1) <= int(range):
                                        listCheck = self.db.lookupCachedURL_byID(int(key1))
                                        if listCheck not in nearList:
                                            nearList.append(listCheck)
                                            break
            except TypeError:
                print("0 results")
        self.print_results(nearList)
        
    def print_results(self, listToPrint):
        itemCount = 0
        for item in listToPrint:
            if item is not None:
                itemCount += 1
                print(str(itemCount) + ". " + str(item))