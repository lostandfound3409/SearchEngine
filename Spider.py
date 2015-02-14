import os
import nltk
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import shutil
from stemming.porter2 import stem
from WebDB import WebDB
import re


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


class Spider:
    directoriesToCreate = [r'data', r'data\item', r'data\raw', r'data\clean',
                           r'data\header']  # Directories to be created
    directoriesToRenew = [r'data\raw', r'data\clean', r'data\header']

    # Constructor, clears and recreates cache
    def __init__(self, create=directoriesToCreate, delete=directoriesToRenew):
        self.delete_dirs(delete)
        self.create_dirs(create)

    #Creates Cache
    def create_dirs(self, directories):
        for direc in directories:
            if not os.path.exists(direc): os.makedirs(direc)
        print("Directories Created!")

    #Deletes Cache
    def delete_dirs(self, directories):
        for direc in directories:
            if os.path.exists(direc): shutil.rmtree(direc)
        print("Cache Cleared!")

    #List parser
    def parser(self, siteIn):
        # Remove scripts and styles
        soup = BeautifulSoup(siteIn)
        [tag.decompose() for tag in soup(["script", "style", "iframe"])]

        s = MLStripper()
        s.feed(str(soup))
        text = s.get_data()
        listChar = ['|', '?', ',', '.', '"', '(', ')', '*', ':', '{', '}', '&', '^', '%', '#', '@', '!', ';', '<', '>',
                    '//', '/', '-', '\\n', '\\t', 'b\'', '©', '=', '==', '\\', '+', '\'', '$', u"\u0148", "[", "]"]
        for badChar in listChar:
            text = text.replace(badChar, " ")
        wordList = nltk.word_tokenize(text)

        return wordList

    #Stemmer
    def stem_list(self, listIn):
        documents = [[stem(word) for word in sentence.split(" ")] for sentence in listIn]
        return documents

    def lower_list(self, listIn):
        lowerList = [token.lower() for token in listIn]
        return lowerList

    def convertEmbeddedList(self, list):
        toReturn = []
        for sublist in list:
            for item in sublist:
                toReturn.append(item)
        return toReturn

    def fetch(self, urlIn, site, id, type):
        print("Fetching...")
        readSite = site.read()

        #Header storage algorithm
        headerFile = open(r'data\header\\' + str(id).zfill(6) + '.txt', 'w+')
        headerFile.write(str(site.info()))
        headerFile.close()


        #Clean
        list = self.parser(readSite)
        list = self.lower_list(list)
        list = self.stem_list(list)
        list = self.convertEmbeddedList(list)
        cleanFile = open(r'data\clean\\' + str(id).zfill(6) + '.txt', 'w+')
        for item in list:
            try:
                cleanFile.write(item + "\n")
                #Raw
                rawFile = open(r'data\raw\\' + str(id).zfill(6) + '.html', 'w+')
                rawFile.write(str(readSite))
                rawFile.close()
            except UnicodeEncodeError:
                print("Non UTF-8 string detected. Not writing to file")
        cleanFile.close()

        #Store in database
        db = WebDB('data\cache.db')
        try:
            titleRE = re.compile("<title>(.+?)</title>")
            title = titleRE.search(str(site)).group(1)
        except AttributeError:
            title = "No title specified"
        urlID = db.insertCachedURL(str(urlIn), "text/html", title)
        itemID = db.insertItem(str(id), type)
        u2iID = db.insertURLToItem(urlID, itemID)
        (url, docType, title) = db.lookupCachedURL_byID(urlID)
        print("Stored in DB \n")
