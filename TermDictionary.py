import math
class TermDictionary():
    def __init__(self):
        self.index = dict()
        self.totalWeight = 0

    #-------------------------------------------
    # Adds a word to the dictionary or updates it if already present
    #-------------------------------------------
    def addWord(self, word, docID, position):
        word = word.strip()
        if word not in self.index:
            self.index[word] = dict()
        if docID not in self.index[word]:
            self.index[word][docID] = list()
            self.index[word][docID].append(0) #Place holder for weight
        self.index[word][docID].append(position)

    def items(self):
        for key in self.index:
            print(key, self.index[key])


    #-------------------------------------------
    # Returns docID's and positional list from a query
    #-------------------------------------------
    def getPosFromQuery(self, query):
        for key, value in self.index.items():
            if (query) == key:
                idList = value
                return idList

    #-------------------------------------------
    # Calculates the weight a search term carries per document
    #-------------------------------------------
    def calcWeight(self, weight):
        for word in self.index:
            for doc in self.index[word]:
                self.index[word][doc][0] = 0
                length = len(self.index[word][doc])
                if weight == "nnn":
                    self.index[word][doc][0] = length - 1
                else:
                    tf = 1 + math.log(length-1)
                    idf = math.log(368 / len(self.index[word])) #Replace 389 with # of total docs
                    tfIdf = (tf * idf)
                    self.index[word][doc][0] = tfIdf
        for word in self.index:
            self.totalWeight = 0
            for doc in self.index[word]:
                self.totalWeight += self.index[word][doc][0] ** 2
            self.totalWeight = math.sqrt(self.totalWeight)

            #Weight of specific document divided by sqrt(sum(weight of all documents in that term^2)
            if weight != "nnn":
                for docAgain in self.index[word]:
                    self.index[word][docAgain][0] /= self.totalWeight

    #-------------------------------------------
    # Calculates the weight of a query in reference to a website
    #-------------------------------------------
    def calcQuery(self, query, weight):
        scores = dict()
        for term in query.split():
            for actualTerm in self.index:
                if term == actualTerm.strip():
                    for doc in self.index[actualTerm]:
                        length = len(self.index[actualTerm][doc])
                        if weight == "nnn":
                            if doc in scores:
                                scores[doc] += self.index[actualTerm][doc][0]
                            else:
                                scores.update({doc: self.index[actualTerm][doc][0]})
                        else:
                            tf = 1 + math.log(length-1)
                            idf = math.log(368 / len(self.index[actualTerm])) #Replace 389 with # of total docs
                            tfIdf = (tf * idf)
                            if doc in scores:
                                scores[doc] += (tfIdf / self.totalWeight) * self.index[actualTerm][doc][0]
                            else:
                                scores.update({doc: (tfIdf / self.totalWeight) * self.index[actualTerm][doc][0]})





        sorted_list = [(k,v) for v,k in sorted([(v,k) for k,v in scores.items()],reverse=True)]
        return sorted_list







