------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This repository contains the files needed to run https://twitter.com/coinshuffle_bot

Apart from the files you need a twitter developer account with read and write permissions activated.

The .csv data files needs to be saved in the same location/directory as stakeShuffle_bot.py.

The data files will need to be updated to one calender day prior to the intended(new) scraping range. At the time of posting this README the .csv files is up to date. 

One of the conditionals in stakeShuffle_bot.py is that it checks the twitter accounts latest tweet for the date in order to determine whether or not to gather and broadcast 
new data. Thus if you run this script for the first time you need to manually tweet the date of the day prior to the first intended broadcast date/scraping range.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
