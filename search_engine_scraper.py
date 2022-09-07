from distutils import file_util
from fileinput import filename
from bs4 import BeautifulSoup
import time
import requests
from random import randint
from html.parser import HTMLParser
import json

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

class SearchEngine:

   @staticmethod
   def search(query, sleep=True):
      if sleep: # Prevents loading too many pages too soon
         time.sleep(randint(10, 50))

      temp_url = '+'.join(query.split()) #for adding + between words for the query
      url = 'http://www.ask.com/web?q=' + temp_url
      soup = BeautifulSoup(requests.get(url, headers= USER_AGENT).text, "html.parser")
      new_results = SearchEngine.scrape_search_result(soup)

      return new_results
 
   @staticmethod
   def scrape_search_result(soup):
      raw_results = soup.find_all("div", attrs = {"class" : "PartialSearchResults-item-title"})
      results = []
      # removes ads and Ask media group results 
      #pre_soup = soup.find(lambda tag: tag.name == 'div' and tag.get('class', '') == ['PartialSearchResults-body'])
      #raw_results = pre_soup.find_all("div", attrs={"class": "PartialSearchResults-item-title"})      
      #results = []
      
   #implement a check to get only 10 results and also check that URLs must not be duplicated
      for result in raw_results:
         link = result.find('a').get('href')
         results.append(link)
      return results

   #return a dictionary with queries ad keys and results as values
   def joinQueriesResults(queryList):
      queryResultDict = {}

      #retrieve search results for each query, store as strings in list
      for query in queryList:
         searchResults = []
         searchResults.append(str(SearchEngine.search(query)))

         #for each query, store the query as the key and results as values in a dictionary
         for result in searchResults:
            queryResultDict.update(query = result)

      return queryResultDict


class InputOutput:

   #return a textfile as a list of strings 
   def parseTextFile(fileName):
      #here is where i parse the queries into an array or something. search takes singular query so i guess call it over iterations of a loop
      queryFile = open(fileName, 'r')
      queryList = []
  
      while True:
         query = str(queryFile.readline())
         queryList.append(query.strip())
         
         #indicates end of file
         if not query:
            queryFile.close()
            break

         
         
      return queryList
  
      

   #reads in JSON file, given name as a string, and returns dictionary
   def parseJSON(fileName):
      with open(fileName) as json_file:
         contents = json.load(json_file)
      
      return contents

   #takes in dictionary and writes to JSON file
   def writeJSON(dictionary):
      with open("AskResults.json", "w") as outfile:
         json.dumps(dictionary, outfile) 
      

def main():
   #create list from textfile containing all queries
   queries = InputOutput.parseTextFile('100QueriesSet3.txt')

   #logging
   print("this is the query list")
   print(queries)

   #not great practice but doing scraping and joining in this function
   print("this is the q/r dictionary")

   qrDict = SearchEngine.joinQueriesResults(queries)

   #logging
   print(qrDict)

   #write Ask data to JSON file
   InputOutput.writeJSON(qrDict)

   #need to compare results
   
   
   

#write query and result pairs from Ask to json file
   #askResultsJSON = writeJSON(INSERT QUERIES AND RESULTS)

if __name__ == "__main__":
    main()
