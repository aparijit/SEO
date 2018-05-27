import nltk
from nltk.corpus import stopwords
import requests, re, json
from bs4 import BeautifulSoup
import networkx as nx
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import html5lib
import operator
#nltk.data.path.append('/home/django2018/nltk_data')
nltk.download('stopwords')
nltk.download('punkt')

'''
import json
from networkx.readwrite import json_graph
'''

import os

def generate_urls(search_string, start):
    # Empty temp list to store the urls
    temp = []

    # url
    url = 'https://www.google.com/search'

    # Parameters in payload
    payload = {'q': search_string, 'start': start}

    # Setting User-Agent
    my_headers = {
        'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    # Getting the response in an Object r
    r = requests.get(url, params=payload, verify=False) #, headers=my_headers, timeout=0.1)
    # Create a Beautiful soup Object of the response r parsed as html
    soup = BeautifulSoup(r.text, 'html.parser')
    # Getting all h3 tags with class 'r'
    h3tags = soup.find_all("h3", {"class": "r"})
    if len(h3tags) == 0 :
        return temp

    # Regular expression for a url
    regex = r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,}'
    twitter_regex = r'http(?:s)?:\/\/(?:www\.)?twitter\.com\/([a-zA-Z0-9_]+)'
    youtube_regex = r'http(?:s)?:\/\/(?:www\.)?youtube\.com\/([a-zA-Z0-9_]+)'
    facebook_regex = r'http(?:s)?:\/\/(?:www\.)?facebook\.com\/([a-zA-Z0-9_]+)'
    for h3 in h3tags:
        try:
            href = h3.a['href']
        except:
            break
        #Discarding twitter, youtube, facebook links shown in search results
        if re.search(twitter_regex, href):
            continue
        elif re.search(youtube_regex, href):
            continue
        elif re.search(facebook_regex, href):
            continue
        # Checking if this a valid link, Sometimes google returns its own suggestions at the top which are not to be considered in the ranking algorithm
        elif re.search(regex, href):
            ''' Pre-processing urls based on the outputs generated of the format:
            /url?q=http://indiatravel.com/&sa=U&ved=0ahUKEwiigPuGhpjbAhWMbysKHdByBtM4ARAWCBMwAA&usg=AOvVaw3QGAr42FfeAr20zv9zB7rT
            '''
            href = href.split("?q=")[1]
            href = href.split("&sa=")[0]
            temp.append(href)

    return temp

def remove_duplicates(result):
    seen = set()
    seen_add = seen.add
    return [x for x in result if not (x in seen or seen_add(x))]

def get_urls(search,pages):
    result = []
    for page in range(0, int(pages)):
        result.extend(generate_urls(search, str(page)))
        if len(result) == 0:
            f = 1
    result = remove_duplicates(result)
    savedurls = []
    for i in result:
        savedurls.append(str(i))
    return savedurls



def googautocomplete(string):
    URL="http://suggestqueries.google.com/complete/search?client=firefox&q="+ string
    headers = {'User-agent':'Mozilla/5.0'}
    response = requests.get(URL, verify=False, headers=headers)
    result = json.loads(response.content.decode('utf-8'))
    suggest = []
    for i in result[1]:
        suggest.append(str(i))
    return suggest

def bs4_soup(url):
    headers = {'User-agent':'Mozilla/5.0'}
    webpage = requests.get(url, veify = False, headers=headers).text
    soup = BeautifulSoup(webpage,"html.parser")
    return soup


def url_title(url):
    headers = {'User-agent':'Mozilla/5.0'}
    soup = BeautifulSoup(requests.get(url, verify= False, headers=headers).text,"html.parser")
    title_tag = soup.find('title')
    title = []
    title.append(title_tag.getText())
    return title


def url_description(url) :
    headers = {'User-agent':'Mozilla/5.0'}
    soup = BeautifulSoup(requests.get(url, verify =False, headers=headers).text,"html.parser")
    meta_tag = soup.findAll('meta')
    meta = []
    for i in meta_tag :
        try :
            match1 = re.match(r'^.*Description.*$', str(i))
            match2 = re.match(r'^.*description.*$', str(i))
            if match1 or match2:
                meta.append(i['content'])
        except :
            g = 0
    return meta



def keyword_analysis(text):
    stop = set(stopwords.words('english'))
    #tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    wordcount={}
    for word in word_tokenize(text):
        word = word.lower()
        if word in stop :
            continue
        if word.isalpha() :
            goahead = True
        else :
            continue
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
    return wordcount


def google_high_rated_phrases(string1,string2):
    search_string=string1 + " " + string2
    return googautocomplete(search_string)


def show_list(search_query, flag):
    key_word_count={}
    key_word_website_count={}
    url_visited=[]
    url_d=[]
    url_visited = get_urls(search_query,1)
    for i in url_visited:
        dict1={}
        url=i
        url = url.replace("https://", "http://")
        my_headers = {
        'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

        soup = BeautifulSoup(requests.get(url, verify=False, headers=my_headers).text,"html.parser")
        meta_tag = soup.findAll('meta')
        meta = []
        for i in meta_tag :
        	try :
        		match1 = re.match(r'^.*Description.*$', str(i))
        		match2 = re.match(r'^.*description.*$', str(i))
        		if match1 or match2:
        			meta.append(i['content'])
        	except :
        		g = 0
        url_d=meta
        if len(url_d)>0:
            dict1=keyword_analysis(url_d[0])
        for key in dict1:
            if key not in key_word_count:
                key_word_count[key]=dict1[key]
            else:
                key_word_count[key]+=dict1[key]
            if key not in key_word_website_count:
                key_word_website_count[key]=1
            else:
                key_word_website_count[key]+=1

    key_word_list = []
    #key_word_count = sorted(key_word_count.items(), key=operator.itemgetter(1))
    for key in key_word_count:
        key_word_list.append(str(key) + " " + str(key_word_count[key]))
    if flag == 2:
        return key_word_list

    key_word_website_list = []
    #key_word__website_count = sorted(key_word__website_count.items(), key=operator.itemgetter(1))
    for key in key_word_website_count:
        key_word_website_list.append(str(key) + " " + str(key_word_website_count[key]))
    if flag == 3:
        return key_word_website_list


    suggest_search_query=[]
    for key in key_word_count:
        suggest_search_query.extend(google_high_rated_phrases(search_query,key))
        suggest_search_query.extend(google_high_rated_phrases(key,search_query))

    '''
        Graph
    '''
    G=nx.Graph()
    nodes={}
    for i in suggest_search_query:
        word_count={}
        word_count=keyword_analysis(i)
        for key in word_count:
            if key not in nodes:
                G.add_node(key)
                nodes[key]=word_count[key]
            else:
                nodes[key]+=word_count[key]
        word=list(word_count)
        for i in range(len(word)-1):
            G.add_edge(word[i],word[i+1])
    print(" ")
    print("NUMBER OF TIMES THE WORD HAS OCCUR")
    print(key_word_count)
    print(" ")
    print("NUMBER OF WEBSITES IN WHICH THE WORDS HAS OCCUR")
    print(key_word_website_count)
    #print(nodes)
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,node_size=50, node_color="red")
    nx.draw_networkx_edges(G,pos,width=1,alpha=0.5,edge_color='yellow')
    nx.draw_networkx_labels(G,pos,font_size=8,font_family='sans-serif')
    plt.axis('off')

    ''' Sigma graph visualization
    d = json_graph.node_link_data(G)
    with open('searchquery/static/query/js/graph.json', 'w') as f:
        json.dump(d, f, indent=4)
    '''
    #fig = plt.figure()
    #os.remove("searchquery/static/query/img/weighted_graph2.jpg")
    strFile = "./searchquery/static/query/img/weighted_graph2.png"
    if os.path.isfile(strFile):
        os.system("rm "+strFile)
    plt.savefig("searchquery/static/query/img/weighted_graph2.png")

    '''
        Graph
    '''

    return suggest_search_query
    # query_list
    # query_list=dict.fromkeys(set(suggest_search_query), [])

##################################################################################

def search_query_title_analysis(search_query):
    key_word_count={}
    key_word_website_count={}
    url_visited=[]
    url_t=[]
    url_visited=get_urls(search_query,1)
    print (url_visited)
    for i in url_visited:
        dict1={}
        url_t=url_title(i)
        if len(url_t)>0:
            dict1=keyword_analysis(url_t[0])
        for key in dict1:
            if key not in key_word_count:
                key_word_count[key]=dict1[key]
            else:
                key_word_count[key]+=dict1[key]
            if key not in key_word_website_count:
                key_word_website_count[key]=1
            else:
                key_word_website_count[key]+=1
    print(" ")
    print("NUMBER OF TIMES THE WORD HAS OCCUR")
    print(key_word_count)
    print(" ")
    print("NUMBER OF WEBSITES IN WHICH THE WORDS HAS OCCUR")
    print(key_word_website_count)
    head=Node(search_query)
    for key in key_word_count:
        layer1=Node(key, parent=head)
    for pre, fill, node in RenderTree(head):
        print("%s%s" % (pre, node.name))
    suggest_search_query=[]
    for key in key_word_count:
        suggest_search_query.extend(google_high_rated_phrases(search_query,key))
        suggest_search_query.extend(google_high_rated_phrases(key,search_query))
    nodes={}
    for i in suggest_search_query:
        word_count={}
        word_count=keyword_analysis(i)
        for key in word_count:
            if key not in nodes:
                G.add_node(key)
                nodes[key]=word_count[key]
            else:
                nodes[key]+=word_count[key]
        word=list(word_count)
        for i in range(len(word)-1):
            G.add_edge(word[i],word[i+1])

    print(nodes)
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,node_size=50, node_color="red")
    nx.draw_networkx_edges(G,pos,width=1,alpha=0.5,edge_color='yellow')
    nx.draw_networkx_labels(G,pos,font_size=8,font_family='sans-serif')
    plt.axis('off')
    plt.savefig("weighted_graph2.png")
    plt.show()
