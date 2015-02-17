import urllib.request
import urllib.error
from Spider import Spider
from MyGoogle import MyGoogle
import os
import time
from TermDictionary import TermDictionary
from sys import exit

import re

my_list = []
wordDict = {}
itemFolder = 'data\item'
cleanFolder = r'data\clean'
googleman = MyGoogle()
id = 0
num_results = 10


for root, dirs, files in os.walk(cleanFolder):
    for file in files:
        count = 0
        log = open(os.path.join(root, file), 'r')
        docID = os.path.splitext(file)[0]
        for term in log.readlines():
            count += 1
            wordDict = TermDictionary()
            wordDict.addWord(term, docID, count, wordDict)
for x in wordDict.items():
    print (x)


choice = int(input("Please enter a number: \n (1)Token \n (2)AND \n (3)OR \n (4)Phrase[2 tokens] \n (5)NEAR \n (6)Download new cache \n (7)Quit \n > "))
while 0 < choice < 8:

    if choice == 1:
        print ("hello")

    #Recreate cache
    elif choice == 6:
        spiderman = Spider()
        for root, dirs, files in os.walk(itemFolder):
            for file in files:
                log = open(os.path.join(root, file),'r')
                type = os.path.splitext(file)[0]
                for query in log.readlines():
                    my_list = googleman.searchMe("\"" + query.rstrip() + "\" " + type)
                    print("Searching for " + "\"" + query.rstrip() + "\" " + type)
                    for url in my_list[0:num_results]:
                        print(url)
                        try:
                            site = urllib.request.urlopen(str(url))
                            spiderman.fetch(url, site, id, type)
                        except urllib.error.URLError:
                            print("Can not access this page, skipping....")
                        id += 1
        print("Please restart the application.")
        time.sleep(5)
    else:
        print ("\nYou did not enter a valid number\n")
        exit(0)

    choice = input("Please enter a number: \n (1)Token \n (2)AND \n (3)OR \n (4)Phrase[2 tokens] \n (5)NEAR \n (6)Download new cache \n (7)Quit \n >")




print("Download Complete!")


