'''
@author Arijit Pramanick, 2017
@project Search Engine Optimisation using Machine Learning

This program crawls google search results based on a search query and lists down the urls of the results in a file called 'scaped_urls.txt'
alongwith their respective rankings.
Crawling can be time consuming. An attempt has been improve performance by implementing parallelism, but crawling rules has t be maintained. 

Requirements:
~ Python 3.4
~ Beautiful Soup 4 : Beautiful Soup sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.
~ Requests : Requests is an Apache2 Licensed HTTP library, written in Python, for human beings. 
~ re : python library for regular expressions
~ urllib : Python library that allows us to send HTTP requests to an web server to get data from the server.

'''

import requests, re
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from docopt import docopt
from time import time as timer
from functools import partial
from multiprocessing import Pool

'''
Fetching data from google using spiders gives HTTP 403: Forbidden error

try:
	url = 'https://www.google.com/search?q=travel+india'
	headers = {}
	headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
#       To get user agent:
# 	<?php
#	echo $_SERVER['HTTP_USER_AGENT']
#	?>
	req = urllib.request.Request(url, headers=headers)
	resp = urllib.request.urlopen(req)
	respData = resp.read()
	saveFile = open('withHeaders.txt','w')
	saveFile.write(str(respData))
	saveFile.close()
except Exception as e:
	print(str(e))
'''


def get_urls(search_string, start):
	#Empty temp list to store the urls
	temp = []
 
	#url
	url = 'https://www.google.com/search'
 
	#Parameters in payload
	payload = { 'q' : search_string, 'start' : start }
 
	#Setting User-Agent
	my_headers = { 'User-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' }
 
	#Getting the response in an Object r
	r = requests.get( url, params = payload, headers = my_headers )
 
	#Create a Beautiful soup Object of the response r parsed as html
	soup = BeautifulSoup( r.text, 'html.parser' )

	#Getting all h3 tags with class 'r'
	h3tags = soup.find_all( "h3", {"class":"r"} )

	#Regular expression for a url 
	regex = r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,}'
	
	for h3 in h3tags:
		href = h3.a['href']
		#Checking if this a valid link, Sometimes google returns its own suggestions at the top which is not to be considered in the ranking algorithm
		if re.search(regex , href) :
			temp.append(href)
	
	return temp
 
def remove_duplicates(result):
	seen = set()
	seen_add = seen.add
	return [x for x in result if not (x in seen or seen_add(x))]

def main():
    start     = timer()

    #Empty List to store the Urls
    result    = []
    search    = input("Enter search string: ")
    pages     = input("Enter no.of pages: ")
    print ("Processing...")
    
    '''
    ####Changes for Multi-Processing####
    processes = input("Enter no. of processes to use (multi-processing) : ")
    processes = int(processes)
    print ("Processing...")
    make_request = partial( get_urls, search )
    pagelist     = [ str(x*10) for x in range( 0, int(pages) ) ]
    with Pool(processes) as p:
        tmp = p.map(make_request, pagelist)
    for x in tmp:
        result.extend(x)
    ####Changes for Multi-Processing####

    '''
    ###For single processing
    #Calling the function [pages] no of times.
    for page in range( 0,  int(pages) ):
        #Getting the URLs in the list
        result.extend( get_urls( search, str(page*10) ) )
    

    #Removing Duplicate URLs
    result    = remove_duplicates(result)
    
    #Printing result set in a file
    saveFile = open('scraped_urls.txt','w')
    rank = 1
    for i in result:
    	saveFile.write(str(rank) +" "+ str(i) + "\n")
    	#print(rank, i)
    	rank += 1
    
    saveFile.close()

    print( '\nTotal URLs Scraped : %s ' % str( len( result ) ) ) 
    print( 'Script Execution Time : %s sec' % ( timer() - start ) )
 
if __name__ == '__main__':
    main()
 
#End 
