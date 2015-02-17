import os

"""
                for file in folder
                count = 0
                    for word in file
                        count++
                        if word exists in dictionary
                            if doc id exists in word
                                append count to list
                            else
                                add page id
                                append count to list
                        else
                            add word to dict
                            add page id
                            add count to list
"""



class TermDictionary():

    def __init__(self, posList, docIDDict,):
        self.posList = posList
        self.docIDDict = docIDDict
        self.wordDict = {}

    def addWord(self, word, docID, posID):
        if word in self.wordDict.keys():
            if docID in self.docIDDict.keys():
                self.posList.append(posID)
                self.wordDict.update({word:{docID: self.posList}})
            else:
                self.docIDDict.update({docID: self.posList.append(posID)})
        else:
            self.wordDict.update({word: {docID: self.posList.append(posID)}})

    def items(self):
        for key in self.wordDict.keys() :
            print (key, "\n")
            for key2 in self.docIDDict.keys():
                print(key2, "\n", self.posList)

