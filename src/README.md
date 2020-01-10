Welcome to the src section. 

Here you will find the ```gr_scraper.py``` and ```gr_db_cleaner.py``` scripts, which collect and clean goodreads user ratings, and the ```samples.txt``` and ```progress.txt```, logfiles that ```gr_scraper.py``` uses. Samples tells gr_scraper which goodreads users to pull data from, and progress records how far the machine has gotten in its current set.

progress.txt is less usefull now that the scraper is crash free, but still very useful so the system can reboot. 

in the data directory, the datacln.npy lives, which is the result of gr_db_cleaner doing its work, and can be ingested into pandas or other software, as it is well behaved data. 
