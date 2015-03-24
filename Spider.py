import os
import urllib.request
import urllib.error
import nltk
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import shutil
from stemming.porter2 import stem
import time
from WebDB import WebDB
from MyGoogle import MyGoogle


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
    directoriesToDelete = [r'data\raw', r'data\clean', r'data\header']
    itemFolder = 'data\item'
    cleanFolder = 'data\clean'
    googleman = MyGoogle()
    startId = 0

    # Constructor
    def __init__(self,):{}

    #-------------------------------------------
    # Create directories
    #-------------------------------------------
    def create_dirs(self, directories):
        for direc in directories:
            if not os.path.exists(direc): os.makedirs(direc)
        print("Directories Created!")

    #-------------------------------------------
    # Delete directories
    #-------------------------------------------
    def delete_dirs(self, directories):
        for direc in directories:
            if os.path.exists(direc): shutil.rmtree(direc)
        print("Cache Cleared!")

    #-------------------------------------------
    # Parses a website and remove unwanted characters
    #-------------------------------------------
    def parser(self, siteIn):
        # Remove scripts and styles
        soup = BeautifulSoup(siteIn)
        title = soup.title.string
        [tag.decompose() for tag in soup(["script", "style", "iframe"])]

        s = MLStripper()
        s.feed(str(soup))
        text = s.get_data()
        listChar = ['|', '?', ',', '.', '"', '(', ')', '*', ':', '{', '}', '&', '^', '%', '#', '@', '!', ';', '<', '>',
                    '//', '/', '-', '\\n', '\\t', 'b\'', '©', '=', '==', '\\', '+', '\'', '$', u"\u0148", "[", "]"]
        for badChar in listChar:
            text = text.replace(badChar, " ")
        wordList = nltk.word_tokenize(text)

        return wordList, title

    def stem_list(self, listIn):
        documents = [[stem(word) for word in sentence.split(" ")] for sentence in listIn]
        return documents

    def lower_list(self, listIn):
        lowerList = [token.lower() for token in listIn]
        return lowerList

    def convert_embedded_list(self, list):
        toReturn = []
        for sublist in list:
            for item in sublist:
                toReturn.append(item)
        return toReturn

    #-------------------------------------------
    # Fetch and store a certain website
    #-------------------------------------------
    def fetch(self, urlIn, site, theId, theType, query):
        wordlist = []
        print("Fetching...")
        readSite = site.read()

        #Header storage
        headerFile = open(r'data\header\\' + str(theId).zfill(6) + '.txt', 'w+')
        headerFile.write(str(site.info()))
        headerFile.close()


        #Clean storage
        wordlist, title = self.parser(readSite)
        wordlist = self.lower_list(wordlist)
        wordlist = self.stem_list(wordlist)
        wordlist = self.convert_embedded_list(wordlist)
        cleanFile = open(r'data\clean\\' + str(theId).zfill(6) + '.txt', 'w+')
        for item in wordlist:
            try:
                cleanFile.write(item + "\n")
            except UnicodeEncodeError:
                print("Non UTF-8 string detected. Not writing to file")
        cleanFile.close()

        #Raw storage
        rawFile = open(r'data\raw\\' + str(theId).zfill(6) + '.html', 'w+')
        rawFile.write(str(readSite))
        rawFile.close()

        #Store in database
        db = WebDB('data\cache.db')
        if title != None:
            title = "".join(c for c in title if c not in ('!','.',':', '\''))
        else:
            title = "No Title Specified"
        query = "".join(c for c in query if c not in ('!','.',':', '\''))
        print(title)
        print (query)
        urlID = db.insertCachedURL(str(urlIn), query + " : " + str(theType), title)
        itemID = db.insertItem(str(theId), theType)
        u2iID = db.insertURLToItem(urlID, itemID)

        print("Stored in DB \n")

    #-------------------------------------------
    # Deletes current cache and recreates it. Function will then initiate
    # the download of the top 10 results for all search terms in the item folder.
    #-------------------------------------------
    def cache_restruct(self):
        input("Are you sure? This will delete all files stored in the data folder \nPress enter to continue.....")
        self.delete_dirs(self.directoriesToDelete)
        self.create_dirs(self.directoriesToCreate)
        databaseClear = input("Would you like to clear the database file as well?(y or n): ")
        if databaseClear == "y":
            db = None
            os.remove('data\cache.db')
            print("Database Cleared!")
        for root, dirs, files in os.walk(self.itemFolder):
            for file in files:
                log = open(os.path.join(root, file), 'r')
                type = os.path.splitext(file)[0]
                for query in log.readlines():
                    my_list = self.googleman.searchMe("\"" + query.rstrip() + "\" " + type)
                    print("Searching for " + "\"" + query.rstrip() + "\" " + type)
                    if my_list is not None:
                        for url in my_list:
                            print(url)
                            try:
                                site = urllib.request.urlopen(str(url))
                                self.fetch(url, site, self.startId, type, query.rstrip())
                            except (urllib.error.URLError, SyntaxError):
                                print("Can not access this page, skipping....")
                                self.startId -= 1
                            self.startId += 1
        print("Please restart the application.")
        time.sleep(5)
