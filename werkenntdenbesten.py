from htmls import *
from bs4 import BeautifulSoup
import json
import requests
import time
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

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

def json_save(dic, file):
    f = open(file, 'w')
    json.dump(dic, f)
    f.close()

def tabulate(csvFile, array):
    with open(csvFile, 'a', newline='' ,encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        for i in range(0, len(array)):
            if len(array[i]) > 0:
                writer.writerow(array[i])
    return True


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
        while page < int(page_end):
            links_hash = search_trade(trade,page,page_hash)
            time.sleep(1)
            page_hash = links_hash["hash"]
            for link in links_hash["links"]:
                links.append(link)
                print(link)
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
    website = str(website).split(",")[1][7:-1].replace("\\","")
    return(website)
