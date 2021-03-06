# Book Readers Are Saps!
### Goodreads user rating biass
<p align="center"> 
<img src="img/goodreads-badge-read-reviews-a8508f765fac427f58da8ebf9e89721a.png">
</p>

I jokingly call book readers saps because they heavily over-rate books in the high ratings range, instead of seeming to have a scale that rates books they've read compared against one another, in a way that create a uniform ranking. This makes choosing a book based on ratings much more challenging than choosing a resturant by rating, where a 3* resturant can be considered a middle of the road resturant...a middle of the road book seems to get more than 4 stars on average. 


I mean, seriously. Look at this. Look what we've done to this ranking system. 

<p align="left">
<img src="img/Thanks_guys.png">

but knowing that we're not rational, heck, I'll assume that the vast majority of people are reviewing books at 4 stars, something more like this. 
<p align="left">
<img src="img/hypothesis_test.png" alt="drawing" width="400">
</p>

#### About Goodreads
Goodreads is a social media platform organized around users who claim to have read books, leave ratings on books, and write reviews about such books. Every user has a page which contains a tabular 'bookshelf' that contains their personal ratings, and lots of additonal book metadata.

Users log onto goodreads and collect the books they've read, and often e-readers ask readers to rate a book as they reach the final pages of the book, and that information, if your accounts are paired, is submitted to goodreads. 

Goodreads reveiws are...slanted. Initially, I expected arguing that book readers are saps, and tend to rate books higher than 4 stars more often than not was a very agressive statement...but its actually rather a lot worse than that.  


## Initial Goal

The project would be, then, to correct for this lean toward a human love of books and de-rank books into a uniform distribution. 

* Collect huge numbers of bookreads user bookshelves
* Prove that book readers are saps through science,
* re-chart their ratings into a sytsem that accounts for their sappy-ness. 

## Hypothesis
Our hypothesis is that goodreads raters rate books above 4 stars more often than not. 

H0 : P(x<=4) > .5
Ha : P(x>4)>.5

## Analys methods 
I  built a scraper to scrape randomly selected user-numbers from the 100m + users on goodreads, pulled their 'bookshelf' book-tablesand stored the html in mongo on a group of ec2. I then built a script which cleans goodreads bookshelf-data created by the scraper does some data engineering to turn the data into easily ingestible .npy files. 

I scraped 13878 user bookshelfs from goodreads, gathering 50109 ratings on 21569 uniqe books (with many popular books having been rated more than once), and ran some data analys on them using Scikit-Learn and Pandas. 



The tech stack consists of Python 3, Numpy, Pandas, Selenium, PyMongo, Beautiful Soup, Scikit-Learn, Matplotlib, HTML
 
scripts in src/:

```gr_scraper.py```
a script which accesses progress.txt and samples.txt as logfiles to scrape the bookshelves of randomly chosen users on goodreads and stores it in mongodb

```gr_db_cleaner.py```
a script which does initial data cleaning and feature engineering, turning the mongo collection into a numpy array. 

Data in src/data/, the cleaned dataset
```datacln.npy```

## Results

A t test was performed on the hypothesis, returning a t statistic of 127.2666, and a P value that rounded to 0. Its very safe to say that goodreads reviews are biassed even more than expected. 


The average rating given to books reviewed in the sample was 4.483 (plus or minus .0074 @95% confidence), and the average rating of books on goodreads, as distinct from the average rating given by a user, is 4.02 (plus or minus .004 @95% confidence)

<p align="center">
<img src="img/simpsons_paradox.png">
</p>
Furthermore, since the average user rating given to books is much higher than the average rating (of all user ratings) for each book, we can conclude, per Simpson's Paradox, that highly reviewed books get more ratings, and a higher porportion of 5 star ratings. This suggests that goodreads actually is working, by leading people to focus on the best books...but in a less than ideal way:

<p align="center">
<img src="img/quantiles.png">
</p>
what you could argue is worthy of a single star review, the lowest 20% of rated books...those books are given between 3.2 and 3.8 average stars….and everything under 3.2 is in the lowest 1% of book reviews


## Future improvements
- use quantile data to generate an api that will respond to user-submitted books with their normalized scoring, ie: I submit Jane Eyre, and the system tells me that *Jane Eyre is among the worst books on goodreads*. More seriously, I expet a response that tells the user what percent of all other books on goodreads that book is ranked higher than, placing it on a graph, and likely a cute response along the lines of the sarcastic and juevenile opinion above. 
- pull review text as well as ratings, and do natural language processing on that to further inform our calculations about the quality of books. 


Finally, anyone who wonders if I fall into this same issue...well, [here's my goodreads shelf,](https://www.goodreads.com/review/list/26338733) which you can see is...primarily 4 and 5 star ratings. 

