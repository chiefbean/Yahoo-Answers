import requests
import json
from bs4 import BeautifulSoup
import db
import pymongo
import scrape
import scroll
import re

URL = 'https://answers.yahoo.com/dir/index?sid='
cats = [
    ('396545012','Arts & Humanities'),
    ('396545144','Beauty & Style'),
    ('396545013','Business & Finance'),
    ('396545311','Cars & Transportation'),
    ('396545660','Computers & Internet'),
    ('396545014','Consumer Electronics'),
    ('396545327','Dining Out'),
    ('396545015','Education & Reference'),
    ('396545016','Entertainment & Music'),
    ('396545451','Environment'),
    ('396545433','Family & Relationships'),
    ('396545367','Food & Drink'),
    ('396545019','Games & Recreation'),
    ('396545018','Health'),
    ('396545394','Home & Garden'),
    ('396545401','Local Businesses'),
    ('396545439','News & Events'),
    ('396545443','Pets'),
    ('396545444','Politics & Government'),
    ('396546046','Pregnancy & Parenting'),
    ('396545122','Science & Mathematics'),
    ('396545301','Social Science'),
    ('396545454','Society & Culture'),
    ('396545213','Sports'),
    ('396545469','Travel'),
    ('396546089','Yahoo Products')
    ]
allLinks = []

database = pymongo.MongoClient("mongodb://localhost:27017/")
table = database["yahoo"]["qs"]

def main():
    global allLinks
    for cat in cats:
        html = scroll.scrollPage(URL+cat[0], 50, 0.75)
        linkSoup = scrape.convertHTML(html)

        for link in linkSoup.find_all('a', class_="QuestionCard__title___1DKC-"):
            if link.get('href').find('question') != -1:
                text = re.sub(r'[^\x00-\x7F]+', ' ', link.text)
                question = [text.encode('utf-8')]
                allLinks.append('https://answers.yahoo.com' + link.get('href'))

        for link in allLinks:
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                question = scrape.findQs(soup, cat[1])
            except Exception:
                continue
            if question is not None:
                db.insert(question, table)
        
        allLinks = []


if __name__=='__main__':
    main()