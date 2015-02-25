class TermDictionary():
    def __init__(self):
        self.index = dict()

    #Adds words, docID, and positional info
    def addWord(self, word, docID, position):
        if word not in self.index:
            self.index[word] = dict()
        if docID not in self.index[word]:
            self.index[word][docID] = list()
        self.index[word][docID].append(position)

    #Prints the items in the structure
    def items(self):
        for key in self.index:
            print(key, self.index[key])

    #Returns docID's and positional list from a query
    def getPosFromQuery(self, query):
        for key, value in self.index.items():
            if (query + "\n") == key:
                idList = value
                return idList




