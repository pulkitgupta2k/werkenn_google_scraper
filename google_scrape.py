from bs4 import BeautifulSoup
from helper import *
from time import sleep

def search_links(term, results_number):
    results = []
    # ps=[]
    term = term.replace(" ","+")
    print(term)
    url = "https://www.google.com/search?q={}".format(term)
    print(url)
    ctr = 0
    while (ctr<int(results_number)):
        try:
            html = getHTML(url)[0]
            soup = BeautifulSoup(html,"html.parser")
            res = soup.findAll('div',{'class':'r'})
            for re in res:
                link = re.find('a')['href']
                # print(link)
                ctr = ctr+1
                results.append(link)
            bottom = soup.find('div', {'id':'foot'})
            next_page = bottom.findAll('a')[-1]
            url = "https://www.google.com{}".format(next_page['href'])
            # print(url)
            sleep(1)
            # for p in ps:
            #     html = getHTML(p)[0]
            #     soup1 = BeautifulSoup(html,"html.parser")
            #     res1 = soup1.findAll('div',{'class':'r'})
            #     for re1 in res1:
            #         link1 = re1.find('a')['href']
            #         results.append(link1)
            #     sleep(1)
        except Exception as e:
            print(e)
            break
    return results