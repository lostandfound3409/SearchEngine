from Spider import Spider
from sys import exit
from WebDB import WebDB
from Queries import Queries

db = WebDB('data\cache.db')
my_list = []
wordDict = {}
id = 190
num_results = 10
queries = Queries()
spiderman = Spider()

choice = int(input("Please enter a number: \n (1)Token \n (2)AND \n (3)OR \n (4)Phrase[2 tokens] \n (5)NEAR \n (6)Download new cache \n (7)Quit \n> "))
while 0 < choice < 8:
    # token query
    if choice == 1:
        queries.token_query()
    #And query
    elif choice == 2:
        queries.and_query()
    #OR query
    elif choice == 3:
        queries.or_query()
    #Phrase Query
    elif choice == 4:
        queries.phrase_query()
    #Near Query
    elif choice == 5:
        queries.near_query()
    #Recreate cache
    elif choice == 6:
        spiderman.cache_restruct()
    elif choice == 7:
        exit(0)

    choice = int(input("Please enter a number: \n (1)Token \n (2)AND \n (3)OR \n (4)Phrase[2 tokens] \n (5)NEAR \n (6)Download new cache \n (7)Quit \n>"))

print("\nYou did not enter a valid number\n")




