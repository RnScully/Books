from pymongo import MongoClient
import pprint
import json
from bs4 import BeautifulSoup
import re
import numpy as np

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



def cleaner():
    '''
    a function that reads in goodreads user review tables gathered
    by the gr_scraper and returns a list for schema
    +++++++++++
    Atributes
    find_lim (int): how many user-reviews to clean. pass 'all' into find lim
                    to clean entire db.   
    +++++++
    Returns
    all_revs: (lst) a list of all the reviews cleaned and schemaed. 

    '''
   

    client = MongoClient('localhost', 27017)
    db=client['reviews']
    collection=db['user_reviews']
    


    documents = [x for x in db['user_reviews'].find()]
    client.close()
    all_revs = []
    for idx, users in enumerate(documents):
        try:
            user = documents[idx]['userid']
        except:
            continue
       
        review_list = documents[idx]['reviews']
        if len(review_list) ==0: #some users have not added any books to their goodreads profile
            sub_rev = [None, None, None, None, None, user, None, None, None]
            all_revs.append(sub_rev)
        else:
            for review in review_list:
                soup = BeautifulSoup(review, 'html.parser')
                title = soup.find_all(class_ = re.compile('title'))[0].text.split('\n')[1].strip()
                try:
                    pages = int(soup.find_all(class_ =re.compile('num_pages'))[0].text.split()[2])
                except:#Some works are infinite scroll documents without pages. 
                    pages = None
                try:
                    isbn = soup.find_all(class_ = re.compile('isbn13'))[0].text.strip('isbn13').strip()
                except: #some works are not given ISBN
                    isbn = None 
                book_type = soup.find_all(class_ = re.compile('format'))[0].text.split('\n')[0].strip()
                author = soup.find_all(class_ = re.compile('author'))[0].text.strip('author ').split('\n')[0]
                av_rate = float(soup.find_all(class_ =re.compile('avg_rating'))[0].text.split()[2])
                num_rate = int(soup.find_all(class_ =re.compile('num_ratings'))[0].text.split()[2].replace(',',''))
                user_rating = str_to_rate(soup.find_all(class_ =re.compile('field rating'))[0].text.split())
                
                sub_rev = [title,author, isbn, book_type, pages, user, user_rating, num_rate, av_rate]
                all_revs.append(sub_rev)
    return all_revs
    
    

     
    
if __name__ == "__main__":
    
    print('hello')
    cleaner()
    print('data cleaned')
    np.save("data/datacln", all_revs) 


