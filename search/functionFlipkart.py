import requests

import urllib
from .models import Flipk, SearchTerm


# constants
token = 'eaeb66c02668485f897d2d948774e760'
url_flp = 'https://affiliate-api.flipkart.net/affiliate/search/json?'


def search_flp(data_flp, keyword):
    for i in range(0, 10):
        id = product_id(data_flp, i)
        name = product_name(data_flp, i)
        link = product_url(data_flp, i)
        st_price = product_stprice(data_flp, i)
        a_price = product_actprice(data_flp, i)
        description = product_description(data_flp, i)
        discount = product_discount(data_flp, i)
        instock = product_instock(data_flp, i)
        brand = product_brand(data_flp, i)
        img = product_image_urls(data_flp, i)

        check = Flipk.objects.filter(p_id=id)

        if link != " " and img != " " and name != " " and a_price != " " and product_id != " ":
            if not check:
                item_flp = Flipk.objects.create(p_link=link, p_name=name, p_img=img, p_id=id, p_discount=discount,
                                                in_stock=instock,
                                                act_price=a_price, st_price=st_price, p_description=description,
                                                p_brand_name=brand)
                item_flp.save()
                st = SearchTerm.objects.get(search_term=keyword)
                item_flp.search_id_flp.add(st)
            else:
                a = Flipk.objects.get(p_id=id)
                st = SearchTerm.objects.get(search_term=keyword)
                a.search_id_flp.add(st)


def make_request_flp(url, keyword):
    new_url = url + urllib.urlencode({'query': keyword}) + '&resultCount=10'
    headers = {"Fk-Affiliate-Id": 'singhmite', "Fk-Affiliate-Token": token}
    jobj = requests.get(new_url, headers=headers).json()
    if jobj:
        return jobj
    else:
        return " "


def product_name(jobj, i):
    p_title = jobj['productInfoList'][i]
    title = p_title['productBaseInfo']['productAttributes']['title']
    if title:
        return title
    else:
        return " "


def product_url(jobj, i):
    p_url = jobj['productInfoList'][i]
    url = p_url['productBaseInfo']['productAttributes']['productUrl']
    if url:
        return url
    else:
        return " "


def product_stprice(jobj, i):
    p_stprice = jobj['productInfoList'][i]
    st_price = p_stprice['productBaseInfo']['productAttributes']['maximumRetailPrice']['amount']
    if st_price:
        return st_price
    else:
        return " "


def product_actprice(jobj, i):
    p_actprice = jobj['productInfoList'][i]
    act_price = p_actprice['productBaseInfo']['productAttributes']['sellingPrice']['amount']
    if act_price:
        return act_price
    else:
        return " "


def product_id(jobj, i):
    p_id = jobj['productInfoList'][i]
    id = p_id['productBaseInfo']['productIdentifier']['productId']
    if id:
        return id
    else:
        return " "


def product_description(jobj, i):
    p_description = jobj['productInfoList'][i]
    p_dsp = p_description['productBaseInfo']['productAttributes']['productDescription']
    if p_dsp:
        return p_dsp
    else:
        return " "


def product_discount(jobj, i):
    p_discount = jobj['productInfoList'][i]
    p_dis = p_discount['productBaseInfo']['productAttributes']['sellingPrice']
    if p_dis:
        return p_dis
    else:
        return " "


def product_instock(jobj, i):
    p_instock = jobj['productInfoList'][i]
    instock = p_instock['productBaseInfo']['productAttributes']['inStock']
    if instock:
        return instock
    else:
        return " "


def product_brand(jobj, i):
    brand = jobj['productInfoList'][i]
    p_brand = brand['productBaseInfo']['productAttributes']['productBrand']
    if p_brand:
        return p_brand
    else:
        return " "


def product_image_urls(jobj, i):
    img = jobj['productInfoList'][i]
    p_img = img['productBaseInfo']['productAttributes']['imageUrls']['400x400']
    if p_img:
        return p_img
    else:
        return " "


