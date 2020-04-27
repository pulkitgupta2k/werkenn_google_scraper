import http
import re
import ssl
# from api_keys import gtmatrix_api
import requests
from requests.auth import HTTPBasicAuth
import time
import json
import csv


gtmatrix_api = {}
with open('gtmatrix_api.json') as f:
    gtmatrix_api = json.load(f)

def json_save(dic, file):
    f = open(file, 'w')
    json.dump(dic, f)
    f.close()

def tabulate_head(csvFile, array):
    with open(csvFile, 'w', newline='' ,encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(array)
    return True

def tabulate(csvFile, array):
    with open(csvFile, 'a', newline='' ,encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(array)
    return True



def getHTML(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    context = ssl._create_unverified_context()
    # # print(url)
    # url = url.encode('utf-8')
    # url = str(url)[2:-1]
    try:
        req = requests.get(url, headers=headers, verify=True)
        try:
            html = req.content.decode('utf-8')
        except:
            html = str(req.content)[2:-1]
        res = []
        res.append(html)
        res.append(False)
        return res
    # except urllib.error.HTTPError as err:
    #     print(err)
    #     return None
    except requests.exceptions.SSLError:
        req = requests.get(url, headers=headers, verify=False)
        html = req.content.decode('utf-8')
        res = []
        res.append(html)
        res.append(True)
        return res
    except Exception as e:
        print(e)
        return None


def get_gtmetrix(url):
    username = gtmatrix_api['username']
    password = gtmatrix_api['password']
    gt_url = "https://gtmetrix.com/api/0.1/test"
    payload = {'url': url, 'x-metrix-adblock': '0'}
    response = requests.request("POST", gt_url, auth=HTTPBasicAuth(username, password) , data = payload)
    response_json = response.json()
    res_url = response_json['poll_state_url']
    imp = {}
    while True:
        try:
            results = requests.get(res_url, auth=HTTPBasicAuth(username, password))
            results_json = results.json()["results"]
            imp["pagespeed_score"] = results_json["pagespeed_score"]
            imp["yslow_score"] = results_json["yslow_score"]
            imp["fully_loaded_time"] = results_json["fully_loaded_time"]
            break
        except:
            time.sleep(1)
            pass
    return imp

def check(link):
    final_res = {}
    page = getHTML(link)
    try:
        html = page[0]
    except:
        print("Error parsing {}".format(link))
        return final_res
    html = html.lower()
    final_res["link"] = link
    final_res["is_wp"] = False
    final_res["invalid_ssl"] = False
    final_res["gtmetrix"] = {}
    if(html.count("wordpress")>0 and html.count("wp-content")>0):
        final_res["is_wp"] = True
    if(page[1]):
        final_res["invalid_ssl"] = True
    if(final_res["is_wp"]):
        final_res["gtmetrix"] = get_gtmetrix(link)
    return(final_res)
    