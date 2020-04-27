from helper import *
from bs4 import BeautifulSoup
import json
import requests
import time
import csv
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

def find_url(string):
    try:
        url = re.search("(?P<url>https?://[^\s]+)", string).group("url")
    except:
        return ""
    return url 

def list_cat(link): #returns the category links
    l = {}
    l['link_cat'] = []
    html = requests.get(link, headers = headers).text
    soup = BeautifulSoup(html,'html.parser')
    cat = soup.find('div',{"data-comment": "Branchen two list"})
    for c in cat.findAll("a"):
        l['link_cat'].append(c['href'])
        print(c['href'])
    return l

def search_trade(trade,page,page_hash):
    links_hash = {}
    links = []
    if page_hash =="":
        url = "https://www.werkenntdenbesten.de/suche?trade={}&location=Deutschland&address_id=1&page={}".format(trade,page)
    else:
        url = "https://www.werkenntdenbesten.de/suche?trade={}&location=Deutschland&address_id=1&page={}&hash={}".format(trade,page,page_hash)
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html,'html.parser')
    res = soup.find("div", {"class" : "results-list"})
    for link in res.findAll('a'):
        if link['href'].startswith('/e/'):
            links.append('https://www.werkenntdenbesten.de'+link['href'])
    links_hash["links"] = links
    links_hash["hash"] = ""
    next_page = soup.find('a', {'class': 'pagination__link pagination__link--next'})
    if next_page.has_attr('data-pagination-hash'):
        links_hash["hash"] = next_page['data-pagination-hash']
    return links_hash

def search_all_trade(trade,page_start, page_end):
    try:
        page = int(page_start)
        links = []
        page_hash = ""
        while page <= int(page_end):
            links_hash = search_trade(trade,page,page_hash)
            time.sleep(1)
            page_hash = links_hash["hash"]
            for link in links_hash["links"]:
                try: 
                    link = find_url(link)
                    links.append(link)
                    print(link)
                except:
                    pass
            print(page)
            page = page + 1
    except Exception as e:
        print(e)
        print("ERROR OCCURED PLEASE TRY AGAIN LATER")
    return links

def get_website(url):
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html,'html.parser')
    website = soup.find("icon-list")
    website = str(website).split(",")[1][7:-1].replace("\\/","/")
    website = find_url(website).replace("&quot","")
    website = website.replace("\\u00e4","ä").replace("\\u00df","ß").replace("\\u00f6","ö").replace("\\00fc","ü").replace("\\00c4","Ä").replace("\\00d6","Ö").replace("\\00dc","Ü")
    print(website)
    return(website)
