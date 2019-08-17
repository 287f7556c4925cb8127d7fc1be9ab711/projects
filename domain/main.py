import shodan
import socket
import os
from pyhunter import PyHunter
import optparse
import json
import requests
import sys

shodan_ports = []
email= []
subdomains = []

def user_option():
    parse = optparse.OptionParser()
    parse.add_option("-d","--domain",dest="domain",help="python3 main.py -d turkhackteam.org             python3 main.py --domain turkhackteam.org")
    options = parse.parse_args()[0]
    if not (options.domain):
        print("domain adresini girin")
        sys.exit()
    return options

def hunter_domain_search(domain):
    api = "44ac9d0fcf060465933c1591d75c2ace4b1692d8"
    hunter = PyHunter(api)
    info = (hunter.account_information())
    print("Kalan API Hakkı : ",info["calls"]["left"])
    print("hunter domain search..")
    while(True):
        if (info["calls"]["left"] != 0):
            result = hunter.domain_search(domain)
            result = result["emails"]
            for i in range(len(result)):
                email.append(result[i]["value"])
            break

        else:
            print("\nMevcut Api Arama Hakkı Bitti")
            print("""
            1 - Yeni API Ekle
            0 - Çıkış Yap
            """)

            choise = input("Yapmak İstediğiniz İşlemi Seçiniz = ")

            if (choise == "1"):
                api = input("\nYeni Api Değerini Giriniz = ")
            elif (choise == "0"):
                break
            else:
                print("Hatalı Bir Seçim Yaptınız, Tekrar Deneyiniz..")



def snov(domain):
    client_id = "13dbcd1d4f2bc66b31b86a1e2beab102"
    client_secret = "b398c425d60d3df3f162ee6775cd3600"
    def get_access_token():
        params = {
            'grant_type':'client_credentials',
            'client_id':client_id,
            'client_secret': client_secret
        }

        res = requests.post('https://app.snov.io/oauth/access_token', data=params)
        resText = res.text.encode('ascii','ignore')

        return json.loads(resText)['access_token']



    def get_domain_search(domain):
        token = get_access_token()
        params = {'access_token':token,
                'domain':domain,
                  'type': 'all',
                  'limit': 1000
        }

        res = requests.post('https://app.snov.io/restapi/get-domain-emails-with-info', data=params)

        return json.loads(res.text)

    print("snow search..")
    result = get_domain_search(domain)
    for i in range(len(result["emails"])):
        email.append(result["emails"][i]["email"])

def shodan_search(domain):
    print("shodan search..")
    ip = socket.gethostbyname(domain)
    API_KEY = "gBlfxwitalzqjaWmTcWeNIOskT55uUqN"
    api = shodan.Shodan(API_KEY)
    host = api.host(ip)
    for i in host["ports"]:
        shodan_ports.append(i)

def sublister(domain):
    print("sublister subdomain search..")
    result = os.popen("python3 sublister/sublist3r.py -d "+domain).read()
    result = result.split()
    for i in result:
        subdomains.append(i)



def main(email,subdomains):
    domain = user_option()
    try:
        hunter_domain_search(domain.domain)
    except:
        pass
    try:
        snov(domain.domain)
    except:
        print("snow API bitti")
    try:
        sublister(domain.domain)
    except:
        pass
    try:
        shodan_search(domain.domain)
    except:
        pass

    email = list(set(email))
    subdomains = list(set(subdomains))

    print(email)
    print(subdomains)
    print(shodan_ports)


if(__name__=="__main__"):
    main(email,subdomains)