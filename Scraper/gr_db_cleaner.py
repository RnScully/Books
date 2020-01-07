from pymongo import MongoClient
import pprint
import json
from bs4 import BeautifulSoup
import re

def str_to_rate(qual_state):
    '''
    a function that turns goodreads's "I liked it" or "I did not like it" star categories
    into the numerical 1-5 rating that they visually imply. 
    ++++++
    Attributes
    qual_state (list) a split string pulled from the beautiful soup output of .text on the rating object
    ++++++
    Returns
    user_rating (int): 1-5 score based on NUMBER OF STARS SELECTED BY THE RATER. I honestly don't understand why that's not the output in the HTML. 
    '''
    if qual_state[-3:] == ['it', 'was', 'amazing']:
        user_rating = 5
    elif qual_state[-3:] ==['really','liked','it']:
        user_rating = 4
    elif qual_state[-2:] ==['liked', 'it']:
        '''note that I belive any that include "really" will be given 4
        before we get to this elif statement, therefore we don't need 
        to worry about the issues of "really liked it" and "liked it"
        overlapping'''
        user_rating= 3
    elif qual_state[-3:]==['it','was','ok']:
        user_rating = 2
    elif qual_state[-3:]==['not','like','it']:
        user_rating = 1
    else:
        user_rating = 0
    return user_rating


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
                pages = int(soup.find_all(class_ =re.compile('num_pages'))[0].text.split()[2])
                av_rate = float(soup.find_all(class_ =re.compile('avg_rating'))[0].text.split()[2])
                num_rate = int(soup.find_all(class_ =re.compile('num_ratings'))[0].text.split()[2].replace(',',''))
                user_rating = str_to_rate(soup.find_all(class_ =re.compile('field rating'))[0].text.split())
                sub_rev = [title, pages, userid, user_rating, num_rate, av_rate]
                all_revs.append(sub_rev)
    return all_revs
