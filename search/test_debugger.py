import re
import bs4 as bs
import requests
import time
import datetime

l = []
with open("india0106.txt", "r") as f:
    for line in f:
        l.append(line)
        



              
base_url = "http://www.amazon.in"
url_azn = "http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords="
query = "bottles"

def make_request_amz(url, query,l):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    main_url = url + query
    for s in l:
        try:
            proxy = s.replace("\n","")
            data = requests.get(main_url, headers=header,proxies={"http":proxy}).content
            data1 = data.decode('utf-8')
            print "got data from" + s
            return data
            break
        except:
            print "trying next proxy in 5 sec"
            time.sleep(5)
    
        

def linkCollector(data):
    link = []
    soup = bs.BeautifulSoup(data, "lxml")
    r1 = soup.find_all('a',{'class':'a-link-normal a-text-normal'})
    for r in r1:
        
        c = r.get('href')
        if 'http://' in c and c not in link:
            link.append(c)
        else:
            continue
    return link

def linkParsser(a,l):
    for i in a:
        p_r = []
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        for s in l:
            try:
                proxy = s.replace("\n","")
                data = requests.get(i, headers=header,proxies={"http":proxy}).content
                data1 = data.decode('utf-8')
                print "got data from" + s
                break
            except:
                print "trying next proxy in 5 sec"
                time.sleep(5)
                
        print i 
        soup = bs.BeautifulSoup(data1,"lxml")
        p_review = soup.find('div',{'class' : 'a-section celwidget'})
        time.sleep(3)
        if p_review:
            p_r.append(p_review)
            while True:
                next_review = p_review.findNext('div', {'class' : 'a-section celwidget'})
                if next_review:
                    p_r.append(next_review)
                    p_review = next_review
                else:
                    break
            count = 0
            for r in p_r:
                count = count + 1
                print count
                t = r.text    
                p = re.search('Was this review helpful to you?', t)
                end = p.start()
                text1 = t[:end]
                heading = "head: " +r_head(text1)
                name = "name: " +r_name(text1)
                date = "date: " + r_date(text1)
                statement = "review: "+r_statement(text1)
                helpful = "help: "+r_helpful(text1)
                tag = "Tags: "+r_tags(text1)
                print heading + "\n" + name +"\n" + date + "\n"+ tag + "\n" + statement + "\n" + helpful
        else:
            print "no reviews yet"

            
            
            
def r_head(data):
    a = re.search("By", data)
    if a:
        end = a.start()
        r_heading = data[:end]
        return r_heading.strip().replace("stars","stars | ")
    else:
        return " "

def r_name(data):
    a = re.search(" on ", data)
    if a:
        end = a.start()
        b = re.search("By", data)
        if b:
            start = b.end()
            reviewer_name = data[start:end]
            return reviewer_name.strip()
        else:
            return " "
    else:
        return " " 

def r_date(data):
    a = re.search(r'\d{4}', data)
    if a :
        end = a.end()
        b = re.search(" on ", data)
        if b:
            start = b.end()
            review_date = data[start:end]
            return review_date.strip()
        else:
            return " "
    else:
        return " "

def r_statement(data):
    a = re.search("Comment", data)
    if a:
        end = a.start()
        b = re.search("Verified Purchase", data)
        if b:
            start = b.end()
            review_statement = data[start:end]
            c = re.search("window.AmazonUIPageJS", review_statement)
            if c:
                end1 = c.start()-1
                r2 = review_statement[:end1]
                if r2 == " ":
                    return "good product.Very useful. i recommend to buy."
                else:
                    return r2.strip()
            else:
                return review_statement.strip()
        else:
            return " "
    else:
        return " "

def r_helpful(data):
    a = re.search("Comment", data)
    if a:
        start = a.end()
        review_helpful = data[start:]
        return review_helpful.strip()
    else:
        return " "

def r_tags(data):
    a = re.search("Verified Purchase", data)
    if a :
        end = a.start()
        d = re.search(r'\d{4}', data)
        if d:
            start = d.end()
            tags = data[start:end]
            return tags.strip().replace("Colour", "  Colour")
        
        else:
            return " "
    else:
        return " "
            
        

    
      


d = make_request_amz(url_azn,query,l)
rone = linkCollector(d)
a = linkParsser(rone,l)




