------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This repository contains the files needed to run <https://twitter.com/StakeShuffle_>

Apart from the files you need a twitter developer account with read and write permissions activated.

The .csv data files needs to be saved in the same location/directory as stakeShuffle_bot.py.

The data files will need to be updated to one calender day prior to the intended(new) scraping/broadcast range. At the time of posting this README the .csv files is up to date. 

Feel free to use csvUpdate.py in this repository to update the csv files. Make sure csvUpdate.py as well as all the csv files are saved in the same directory
on your system. Its a user friendly GUI(graphical user interface) to assist in updating the csv data-files in this repo. I have only tested in on Linux. 
It will likely not work/error if you run it from an IDE like IDLE. Open a terminal from within the location of where you saved the above-mentioned files and exceute 
it from within the terminal.

See { csv_update1.png ; csv_update2.png ; csv_update3.png ; csv_update4.png } in this repository for screenshot examples on how to use this GUI helper.

Be sure to pip install the following python libraries otherwise you will likely get errors when running the python files in this repository.

-easygui
-progressbar
-BeautifulSoup / bs4
-tweepy
-pandas
-itertools
-numpy
-matplotlib

One of the conditionals in stakeShuffle_bot.py is that it checks the twitter accounts latest tweet for the date in order to determine whether or not to gather and broadcast 
new data. Thus if you run this script for the first time you need to manually tweet the date of the day prior to the first intended broadcast date/scraping range.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
