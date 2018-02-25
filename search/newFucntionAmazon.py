import bs4 as bs
import requests

url_azn = "http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
raw_url = "http://www.amazon.in"


def make_request_eby(url, query):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    main_url = url + query
    data = requests.get(main_url, headers=header).content
    data1 = data.decode('utf-8')
    return data1


def correct_keyword_amz(data):
    soup = bs.BeautifulSoup(data, "html.parser")
    c_word = soup.find('a', {'class': 'a-link-normal a-text-normal'}).text
    if c_word != " ":
        return c_word
    else:
        return " "
#
# def linkCollector(data):




