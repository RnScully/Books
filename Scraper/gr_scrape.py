'''a script which scrapes a user's reviews given user ID number, a simple int from 1 to over 100m, each a unique goodreads user ID'''

import selenium
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
from pymongo import MongoClient

#hacky way to easily edit the range to operate over in nano on the ec2



def click_in_margin():
    '''gets rid of an annoying pop-up that asks you to log in whenever you load a page'''
    actions.move_by_offset(25,150).perform()
    actions.click()
    actions.move_by_offset(-25,-150).perform()


def scroll_to_bottom(scroll_wait):
    '''a function which rolls through a page to force the lazy loader to load everything'''
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        time.sleep(scroll_wait) #wait for page to load
        
        last_height = new_height

def scoop_reviews():
    '''a function to take the page of reviews and dump it into mongodb'''
    # pull all class objects called 'bookalike review' into a list 
    reviews = driver.find_elements_by_class_name("bookalike")
    #turn the bookalikes into json lists
    jsons = [items.get_attribute('outerHTML') for items in reviews]
  
    doc = {'userid':gr_userid, 'reviews' : jsons}
    return doc


def log_current_sample():
    'a simple helperfunction that keeps track of where in the sampling order we are'
    with open('progress.txt', 'w')as f:
        f.write(str(current_index))

def import_samples():
    'takes the list of samples and turns them into a workable list'
    samples = np.loadtxt('samples.txt')
    return [int(items) for items in samples]

def get_last_index():
    'checks our progress for system restarts'
    return int(np.loadtxt('progress.txt'))    

#create an option to run the script without a window (headless mode)
option = webdriver.FirefoxOptions()
option.add_argument('-headless')
print("Hello, I'm just getting everything together")
driver =  webdriver.Firefox(options=option)
actions = ActionChains(driver)



first_page = True

samples = import_samples()
current_index=get_last_index()
stop_index = len(samples)-1
while current_index < stop_index:

    print("**stretches**")
    current_index  +=1
    log_current_sample()
    gr_userid = samples[current_index]
    ratings_url = 'https://www.goodreads.com/review/list/{}?sort=rating&view=reviews'.format(gr_userid)
    print('trying to load '+ratings_url)
    driver.get(ratings_url)
    '''
    try:
        driver.get(ratings_url) #try to load the pagehttps://stackoverflow.com/questions/48277451/selenium-c-sharp-how-to-tell-selenium-that-we-have-been-redirected-to-another
    except:
        continue
    '''
    
    if (str(gr_userid)in driver.current_url) != True:
        print("Uhhh....I'm a little confused, but somehow I ended up at {}".format(driver.current_url))
        continue
    

    if first_page == True:
        click_in_margin()
        first_page =False
    

    
    print('scrolling down')
    scroll_to_bottom(1.5)  # let the website load for 1.5 secs...ugh
    print('scooping reveiws')

    #connect to the mongo thing
    client = MongoClient()
    db = client['reviews']
    gr_collection = db['user_reviews']
    gr_collection.insert_one(scoop_reviews()) 
    #add doc to mongodb
    print("finshed scooping user {}, but now I'm sleepy".format(gr_userid))
    #disconnect from mongo(do this over and over, don't keep mongo open, hopefully saves ram!?)
    driver.close()

    time.sleep(3) #sleep of 4 felt too long. see if 3 gets you kicked. 
#end loop


