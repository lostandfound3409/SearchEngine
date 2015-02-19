class TermDictionary():

    def __init__(self):
        self.index = dict()

    def addWord(self, word, docID, position):
        if word not in self.index:
            self.index[word] = dict()
        if docID not in self.index[word]:
            self.index[word][docID] = list()
        self.index[word][docID].append(position)

    def items(self):
        for key in self.index :
            print(key, self.index[key])

