import re
import locale
import requests

from .models import Amz, SearchTerm


url_azn = "http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
locale.setlocale(locale.LC_ALL, '')


def make_request_azn(url, word):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'}
    url += word
    data = requests.get(url, headers=header).content
    data1 = data.decode("utf-8")
    return data1


def proper_word(a):
    proper_word1 = re.sub(' +', ' ', a)
    return proper_word1


def search_term_view(keyword):
    check_st = SearchTerm.objects.filter(search_term=keyword)
    if check_st:
        return 1
    else:
        return 0


def search_amz(data1, keyword):
    for i in range(0, 50):
        j = i + 1
        results = get_result_amz(i, j, data1)
        if results == " ":
            return " "
        else:
            item_creator_amz(results, keyword)


def item_creator_amz(results, keyword):
    ret = " "

    # getting the data from functions

    link = get_link_amz(results)
    image = get_img_amz(results)
    name = get_name_amz(results)
    a_price = get_price_amz(results)
    product_id = get_p_id_amz(link)
    st_price = "Rs. " + get_stprice_amz(results)
    review = get_review_amz(results)

    check = Amz.objects.filter(p_id=product_id)

    category_spon = re.search('Sponsored', results)
    if category_spon:
        return ret
    category_shop = re.search('Shop by Category', results)
    if category_shop:
        return ret

    elif link != " " and image != " " and name != " " and a_price != " " and product_id != " ":

        if not check:
            if st_price == '5' or st_price == "5" or st_price == 'Rs. 5':
                st_price = "Rs. MRP"
            item_amz = Amz.objects.create(p_link=link, p_name=name, p_img=image, p_id=product_id,
                                          act_price=a_price, review=review, st_price=st_price)
            item_amz.save()
            st = SearchTerm.objects.get(search_term=keyword)
            item_amz.search_id_amz.add(st)
        else:
            a = Amz.objects.get(p_id=product_id)
            st = SearchTerm.objects.get(search_term=keyword)
            a.search_id_amz.add(st)

    else:
        return ret


# Amazon Functions From here

def correct_keyword_amz(a):
    right_s = re.search('didYouMean', a)
    if right_s:
        start = right_s.end() + 50
        end = start + 250
        dem1 = a[start:end]
        right_s1 = re.search('">', dem1)
        if right_s1:
            right_e = re.search('</a>', dem1)
            if right_e:
                start1 = right_s1.end()
                end1 = right_e.start()
                dem2 = dem1[start1:end1]
                return dem2
            else:
                return " "
    else:
        return " "


def get_result_amz(i, j, data1):
    s = re.search('result_' + str(i), data1)
    if s:
        start = s.end() + 58
        e = re.search('result_' + str(j), data1)
        if e:
            end = e.start()
            result = data1[start:end]
        else:
            result = " "
            return result
    else:
        result = " "
        return result

    return result


def get_link_amz(a):
    link_s = re.search('a-link-normal a-text-normal" href="', a)
    if link_s:
        start1 = link_s.end()
        end1 = start1 + 1000
        dem1 = a[start1:end1]
        link_e = re.search('">', dem1)
        if link_e:
            end = link_e.start()
            link = dem1[:end] + "&tag=del0f0-21"
        else:
            link = " "
    else:
        link = " "
    return link


def page_change_azn(a):
    page_ch_s = re.search('pagnCur', a)
    start = page_ch_s.end() + 71
    end1 = start + 600
    dem1 = a[start:end1]
    page_ch_e = re.search('</a>', dem1)
    end = page_ch_e.start() - 4
    page_ch = dem1[:end]
    page_ch_url = "http://www.amazon.in" + page_ch
    return page_ch_url


def get_name_amz(a):
    name_s = re.search('normal">', a)
    if name_s:
        start = name_s.end()
        name_e = re.search('</h2>', a)
        end = name_e.start()
        name = a[start:end]
    else:
        name = " "
    return name


def get_img_amz(a):
    img_s = re.search('<img src="', a)
    if img_s:
        start = img_s.end()
        img_e = re.search('.jpg', a)
        end = img_e.end()
        image = a[start:end]
    else:
        image = " "
    return image


def get_price_amz(a):
    price_s = re.search('currencyINR">', a)
    if price_s:
        start = price_s.end() + 19
        end1 = start + 20
        dem1 = a[start:end1]
        price_e = re.findall(r'\d+', dem1)
        if price_e[-1] == "00":
            del price_e[-1]
            price_e1 = ''.join(price_e)
            print price_e1 + "Second"
            price_e2 = locale.format("%d", float(price_e1), grouping=True)
        else:
            # del price_e[-1]
            price_e1 = ''.join(price_e)
            print price_e1
            price_e2 = locale.format("%d", float(price_e1), grouping=True)

    else:
        price_e2 = " "
    return price_e2


def get_stprice_amz(a):
    st_price_s = re.search('a-text-strike">', a)
    if st_price_s:
        start = st_price_s.end() + 45
        end1 = start + 20
        dem1 = a[start:end1]
        st_price = re.findall(r'\d+', dem1)
        if st_price:
            if st_price[-1] == "00":
                del st_price[-1]
                st_price1 = ''.join(st_price)
                st_price2 = locale.format("%d", float(st_price1), grouping=True)

            elif st_price[-1] == "99":
                price_e2 = str(float(st_price[0]) + 1)
                st_price1 = ''.join(price_e2)
                st_price2 = locale.format("%d", float(st_price1), grouping=True)

            else:
                st_price1 = ''.join(st_price)
                st_price2 = locale.format("%d", float(st_price1), grouping=True)
        else:
            st_price2 = "MRP"
    else:
        st_price2 = "MRP"
    return st_price2


def get_review_amz(a):
    review_s = re.search('out of 5 stars', a)
    if review_s:
        start = review_s.end()
        end1 = start - 30
        dem1 = a[end1:start]
        review_e = re.search('">', dem1)
        start = review_e.end()
        review = dem1[start:]
    else:
        review = "No Reviews yet"

    return review


def get_p_id_amz(a):
    p_id_s = re.search('/dp/', a)
    if p_id_s:
        start = p_id_s.end()
        end = start + 10
        product_id = a[start:end]
    else:
        product_id = " "
    return product_id


def word_seperator_all(a):
    word = a.split()
    last_word = word[-1]
    return last_word
