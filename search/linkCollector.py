import re
import bs4 as bs
import requests

base_url = "http://www.amazon.in"
url_azn = "http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
query = "mouse"

def make_request_amz(url, query):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    main_url = url + query
    data = requests.get(main_url, headers=header).content
    data1 = data.decode('utf-8')
    return data1


def pageChange(data):
    base_url = "http://www.amazon.in"
    soup = bs.BeautifulSoup(data,"html.parser")
    r = soup.find('span',{'class':'pagnLink'}).a['href']
    next_url = base_url+r
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data1 = requests.get(next_url, headers=header).content
    data2 = data1.decode('utf-8')
    return data2

def linkCollector(data):
    link = []
    soup = bs.BeautifulSoup(data, "html.parser")
    r1 = soup.find_all('a',{'class':'a-link-normal a-text-normal'})
    for r in r1:
        c = r.get('href')
        if 'http://' in c and c not in link:
            link.append(c)
        else:
            continue
    return link

def nextPageLinks(data):
    links = []
    d1 = pageChange(data)
    
    r1 = linkCollector(d1)
    d2 = pageChange(d1)
    r2 = linkCollector(d2)
    d3 = pageChange(d2)
    r3 = linkCollector(d3)
    d4 = pageChange(d3)
    r4 = linkCollector(d4)
    rf = r1+ r2 + r3 + r4
    return rf
count = 0
i = 0
rone = []
rfour = []
d = make_request_amz(url_azn,query)
rone = linkCollector(d)
rfour = nextPageLinks(d)
rfinal = rone + rfour
for a in rfinal:
    i = i+1
    print a
    print i
