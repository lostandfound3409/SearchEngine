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



class TermDictionary:
    word = ""
    docID = ""
    posID = ""


    def __init__(self, word, docID, posID, posList, **wordDict, **docIDDict):
        word = word
        docID = docID
        posID = posID
        posList = posList
        docIDDict = docIDDict
        termDict = wordDict

    def addWord(self):
        if self.word in self.termDict.keys():
            if self.docID in self.docIDDict.keys():
                self.posList.append(self.posID)
                self.termDict.update({self.word:{self.docID: self.posList}})
            else:
                self.docIDDict.update({self.docID: self.posList.append(self.posID)})
        else:
            self.termDict.update({self.word: {self.docID: self.posList.append(self.posID)}})

        return self.termDict

