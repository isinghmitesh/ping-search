import urllib2
import json
from bs4 import BeautifulSoup


def get_soup(url, header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers=header)), 'html.parser')


query = raw_input("query image")  # you can change the query for the image  here
image_type = "ActiOn"
query = query.split()
query = '+'.join(query)
url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
print url
# add the directory for your image here
DIR = "Pictures"
header = {
'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
soup = get_soup(url, header)

ActualImages = []  # contains the link for Large original images, type of  image
for a in soup.find_all("div", {"class": "rg_meta"}):
    link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
    ActualImages.append((link, Type))

print  ActualImages,
