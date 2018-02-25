import re
import locale
import requests
from .models import Snd, SearchTerm


url_snd = "https://www.snapdeal.com/search?keyword="
locale.setlocale(locale.LC_ALL, '')


def proper_word(a):
    proper_word1 = re.sub(' +', ' ', a)
    return proper_word1


# Snapdeal Data Fetching

def search_snd(data1, keyword):
    for i in range(0, 50):
        j = i + 1
        results = get_result_snd(i, j, data1)
        if results == " ":
            return " "
        else:
            item_creator_snd(results, keyword)


def item_creator_snd(results, word1):
    # getting the data from functions

    link = get_link_snd(results)
    image = get_img_snd(results)
    name = get_name_snd(results)
    a_price = get_price_snd(results)
    product_id = get_p_id_snd(results)
    st_price = get_stprice_snd(results)

    review = get_review_snd(results)

    check = Snd.objects.filter(p_id=product_id)

    if link != " " and image != " " and name != " " and a_price != " " and product_id != " ":

        if not check:
            item_snd = Snd.objects.create(p_link=link, p_name=name, p_img=image, p_id=product_id,
                                          act_price=a_price, review=review, st_price=st_price)
            item_snd.save()
            st = SearchTerm.objects.get(search_term=word1)
            item_snd.search_id_snd.add(st)

        else:
            s = Snd.objects.get(p_id=product_id)
            st = SearchTerm.objects.get(search_term=word1)
            s.search_id_snd.add(st)

    else:
        return " "


# Snapdeal Functions From here


def make_request_snd(url, query):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'}
    url += query
    data = requests.get(url, headers=header).content
    data1 = data.decode("utf-8")
    return data1


def get_result_snd(i, j, data1):
    s = re.search('data-js-pos="' + str(i), data1)
    if s:
        start = s.start() - 18
        e = re.search('data-js-pos="' + str(j), data1)

        if e:
            end = e.start()
            result = data1[start:end]
        else:
            result = " "
            return result
    else:
        return " "

    return result


def get_link_snd(a):
    link_s = re.search('href="', a)
    if link_s:
        start = link_s.end()
        link_e = re.search('data-position=', a)

        if link_e:
            end = link_e.start() - 2
            link = a[start:end]
        else:
            link = " "
    else:
        link = " "
    return link


def page_change_snd(a):
    page_ch_s = re.search('pagnCur', a)
    start = page_ch_s.end() + 71
    end1 = start + 600
    dem1 = a[start:end1]
    page_ch_e = re.search('</a>', dem1)
    end = page_ch_e.start() - 4
    page_ch = dem1[:end]
    page_ch_url = "http://www.amazon.in" + page_ch
    return page_ch_url


def get_name_snd(a):
    name_s = re.search('product-title', a)
    if name_s:
        start1 = name_s.end()
        end1 = start1 + 1000
        dem1 = a[start1:end1]
        name_e = re.search('">', dem1)
        start = name_e.end()
        name_e1 = re.search('</p>', dem1)
        end = name_e1.start()
        name = dem1[start:end]
    else:
        name = " "
    return name


def get_img_snd(a):
    img_s = re.search('srcset="', a)
    if img_s:
        start = img_s.end()
        img_e = re.search('" title=', a)
        end = img_e.start()
        image = a[start:end]
    else:
        image = " "
    return image


def get_stprice_snd(a):
    st_price_s = re.search('price strike', a)
    if st_price_s:
        start = st_price_s.end() + 3
        end1 = start + 30
        dem1 = a[start:end1]
        p = re.search('</span>', dem1)
        end = p.start()
        st_price = dem1[:end]
    else:
        st_price = "Rs. MRP"
    return st_price


def get_price_snd(a):
    price_s = re.search('display-price="', a)
    if price_s:
        start = price_s.end()
        end1 = start + 20
        dem1 = a[start:end1]
        price_e = re.search('"', dem1)
        end = price_e.start()
        price_act = dem1[:end]
        price_e2 = locale.format("%d", float(price_act), grouping=True)
    else:
        price_e2 = " "
    return price_e2


def get_review_snd(a):
    review_s = re.search('style="width:', a)
    if review_s:
        start = review_s.end()
        end1 = start + 10
        dem1 = a[start:end1]
        review_a1 = str(float(''.join(re.findall(r'\d+', dem1))) / 10)
        review_act = review_a1[:2] + "/100"
    else:
        review_act = "No Reviews yet"

    return review_act


def get_p_id_snd(a):
    p_id_s = re.search('pogId="', a)
    if p_id_s:
        start = p_id_s.end()
        end = start + 12
        product_id = a[start:end]
    else:
        product_id = " "
    return product_id






