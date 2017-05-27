from bs4 import BeautifulSoup
from yelpapi import YelpAPI
import requests
import re
import urllib
import configparser
import sys

config = configparser.ConfigParser()
config.sections()
config.read('settings.ini')
secret = config['creds']['secret']
client = config['creds']['client']

yelp_api = YelpAPI(client, secret)
regex = '(\/biz_redir)(.*)(url=)(.*)(&website)(.*)'
term = sys.argv[1]
zipcode = "94086"


def printurl(site):
    if '/biz_redir?url=' in str(site):
        match = re.search(regex,site)
        print urllib.unquote(urllib.unquote(match.group(4)))

def parselinks(sites):
    r = requests.get(sites)
    data = r.text
    soup = BeautifulSoup(data,"lxml")
    for link in soup.find_all('a'):
        printurl(link.get('href'))

def yelp():
    results = yelp_api.search_query(term=term, location=zipcode)
    for business in results["businesses"]:
        if business["url"]:
            parselinks(business["url"])


yelp()