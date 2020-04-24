from urllib.request import Request, urlopen
import urllib.request
import http
import re
import ssl
from api_keys import gtmatrix_api
import requests
from requests.auth import HTTPBasicAuth
import time

def getHTML(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url=url, headers=headers)
    context = ssl._create_unverified_context()
    try:
        html = urlopen(req).read().decode('ascii', 'ignore')
        res = []
        res.append(html)
        res.append(False)
        return res
    except urllib.error.HTTPError as err:
        print("%s for %s" % (err.code, url))
        return None
    except urllib.error.URLError:
        html = urlopen(req, context=context).read().decode('ascii', 'ignore')
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
