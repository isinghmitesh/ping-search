import re

import bs4 as bs
import requests

from .models import Ebay, SearchTerm


url_eby = 'http://www.ebay.in/sch/i.html?_nkw='
query = 'belt'


def make_request_eby(url, query):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    main_url = url + query
    data = requests.get(main_url, headers=header).content
    data1 = data.decode('utf-8')
    return data1


def search_eby(data, keyword):
    for i in range(1, 50):
        name_s = re.search('r="' + str(i) + '"', data)
        if name_s:
            start = name_s.end()
            data1 = data[start:]
            item_creator_eby(data1, keyword) #test git
        else:
            data1 = " "
            return data1


def item_creator_eby(data1, keyword):
    soup = bs.BeautifulSoup(data1, "html.parser")
    product_id = soup.div['iid']
    link = soup.a['href']
    img = soup.img['src']
    name = soup.img['alt']
    act_price = soup.find('span', {'class': 'bold'}).text
    hotness = soup.find('div', {'class': 'hotness-signal red'})
    if hotness:
        hotness1 = soup.find('div', {'class': 'hotness-signal red'}).text.replace("'" and "[" and "]", "").strip()
    else:
        hotness1 = " "

    check = Ebay.objects.filter(p_id=product_id)

    if link and img and name and act_price and product_id:
        if not check:
            item_eby = Ebay.objects.create(p_id=product_id, p_name=name, p_link=link, p_img=img, mrp=" ",
                                           act_price=act_price, p_description=" ", p_hotness=hotness1)
            item_eby.save()
            st = SearchTerm.objects.get(search_term=keyword)
            item_eby.search_id_eby.add(st)
        else:
            a = Ebay.objects.get(p_id=product_id)
            st = SearchTerm.objects.get(search_term=keyword)
            a.search_id_eby.add(st)

    else:
        return " "


