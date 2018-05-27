This program crawls google search results based on a search query and lists down the urls of the results in a file called 'scaped_urls.txt'
alongwith their respective rankings.
Crawling can be time consuming. An attempt has been improve performance by implementing parallelism, but crawling rules has to be maintained. Too many requests at a time jams the server.

Requirements:
~ Python 3.4
~ Beautiful Soup 4 : Beautiful Soup sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.
~ Requests : Requests is an Apache2 Licensed HTTP library, written in Python, for human beings. 
~ re : python library for regular expressions
~ urllib : Python library that allows us to send HTTP requests to an web server to get data from the server.

Compile using : python search.py
