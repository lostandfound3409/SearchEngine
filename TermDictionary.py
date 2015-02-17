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

    def addWord(self, word, docID, posID, posList, wordDict, docIDDict):
        if word in wordDict.keys():
            if docID in docIDDict.keys():
                posList.append(posID)
                wordDict.update({word:{docID: posList}})
            else:
                docIDDict.update({docID: posList.append(posID)})
        else:
            wordDict.update({word: {docID: posList.append(posID)}})

        return wordDict

