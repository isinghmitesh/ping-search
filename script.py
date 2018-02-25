# fo = open("search_term.txt",'wr')
# for i in s:
#     x = len(i.search_term)
#     if x>3:
#         fo.write(i.search_term+"\n")
# fo.close()

import requests
url="http://127.0.0.1:8000/product/?search_term=soap"
with open("search_term.txt",'r') as f:
    for line in f:
        url = url +line
        response = requests.get(url)
        print "searching..."+line
        if response.ok:
            print "success"
