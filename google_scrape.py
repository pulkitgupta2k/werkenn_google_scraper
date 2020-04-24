from bs4 import BeautifulSoup
from helper import *
from time import sleep

def search_links(term):
    results = []
    ps=[]
    term = term.replace(" ","+")
    print(term)
    url = "https://www.google.com/search?q={}".format(term)
    html = getHTML(url)[0]
    soup = BeautifulSoup(html,"html.parser")
    bottom = soup.find('div', {'id':'foot'})
    pages = bottom.findAll('a')
    for page in pages:
        ps.append("https://www.google.com{}".format(page['href']))
    res = soup.findAll('div',{'class':'r'})
    for re in res:
        link = re.find('a')['href']
        results.append(link)
    sleep(1)
    for p in ps:
        html = getHTML(p)[0]
        soup1 = BeautifulSoup(html,"html.parser")
        res1 = soup1.findAll('div',{'class':'r'})
        for re1 in res1:
            link1 = re1.find('a')['href']
            results.append(link1)
        sleep(1)
    return results