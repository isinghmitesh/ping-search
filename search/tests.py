import re
import ast
import time

import bs4 as bs
import requests


l = []
with open("india0406.txt", "r") as f:
    for line in f:
        l.append(line)

base_url = "http://www.amazon.in"
url_azn = "http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
query = "bottles"


def make_request_amz(url, query, l):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    main_url = url + query
    for s in l:
        try:
            proxy = s.replace("\n", "")
            data = requests.get(main_url, headers=header, proxies={"http": proxy}).content
            print "got data from" + s
            return data
        except:
            print "trying next proxy in 5 sec"
            time.sleep(5)


def linkCollector(data):
    link = []
    soup = bs.BeautifulSoup(data, "lxml")
    r1 = soup.find_all('a', {'class': 'a-link-normal a-text-normal'})
    for r in r1:
        c = r.get('href')
        if 'http://' in c and c not in link:
            link.append(c)
        else:
            continue
    return link


def imageCollector(a, l):
    for i in a:
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        for s in l:
            try:
                proxy = s.replace("\n", "")
                data = requests.get(i, headers=header, proxies={"http": proxy}).content
                print "got data from" + s
                break
            except:
                print "trying next proxy in 5 sec"
                time.sleep(5)

        JSON = re.compile('var data = ({.*?})]}', re.DOTALL)
        matches = JSON.search(data)
        dic = str(matches.group(1)[47:]).replace("\"", "'")
        f_dic = dic.split("'lowRes':null}")
        if f_dic:
            for c in range(0, 10):
                s = f_dic[c]
                if s:
                    st = s[:-1] + "}"
                    if st[0] == ",":
                        st = s[1:-1] + "}"
                        if 'null' in st:
                            new_st = st.replace('null', "'null'")
                            r_dic = ast.literal_eval(new_st)
                            print "large " + r_dic['large']
                        else:
                            r_dic = ast.literal_eval(st)
                            print "hiRes " + r_dic['hiRes']
                            print "large " + r_dic['large']

                    else:
                        if 'null' in st:
                            new_st = st.replace('null', "'null'")
                            r_dic = ast.literal_eval(new_st)
                            print "large " + r_dic['large']
                        else:
                            r_dic = ast.literal_eval(st)
                            print "hiRes " + r_dic['hiRes']
                            print "large " + r_dic['large']
                else:
                    return " "


d = make_request_amz(url_azn, query, l)
rone = linkCollector(d)
imageCollector(rone, l)
