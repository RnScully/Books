from pymongo import MongoClient
import pprint
import json
from bs4 import BeautifulSoup
import re

def gr_db_cleaner(find_lim = 10):
    '''
    a function that reads in goodreads user review tables gathered
    by the gr_scraper and returns a list for schema
    +++++++++++
    Atributes
    find_lim (int): how many user-reviews to clean.  
    +++++++
    '''
    
    client = MongoClient('localhost', 27017)
    db=client['reviews']
    collection=db['user_reviews']

    documents = [x for x in collection.find().limit(find_lim)]
    all_revs = []
    for idx, users in enumerate(documents):
        userid = documents[idx]['userid']
        review_list = documents[idx]['reviews']
            if len(review_list) ==0:
                sub_rev = [None, None, userid, None, None, None]
                all_revs.append(sub_rev)
            else:
                for review in review_list:
                    soup = BeautifulSoup(review, 'html.parser')
                    title = soup.find_all(class_ = re.compile('title'))[0].text
                    pages = soup.find_all(class_ =re.compile('num_pages'))[0].text
                    av_rate = soup.find_all(class_ =re.compile('avg_rating'))[0].text
                    num_rate = soup.find_all(class_ =re.compile('num_ratings'))[0].text
                    user_rating = soup.find_all(class_ =re.compile('field rating'))[0].text
                    sub_rev = [title, pages, userid, user_rating, num_rate, av_rate]
                    all_revs.append(sub_rev)
    return all_revs
