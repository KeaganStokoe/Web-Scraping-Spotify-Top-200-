# _______________________________________________ Creating a Spotify Chart Scraper _____________________________________________________________

import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from time import time
from time import sleep
from random import randint
import pandas as pd

# _______________________________________________ Set the URL & dates to be scraped _____________________________________________________________________

base_url = 'https://spotifycharts.com/regional/za/daily/'
start = date(2019, 1, 1)
end = date(2019, 12, 31)

iter = timedelta(days=1)

start_time = time()
serve = 0

mydate = start

while mydate < end:

    if(mydate > end):
        break

    # combining base_url with the formatted mydate variable to get each iteration of dates for the whole dataset

    r = requests.get(base_url + mydate.strftime('%Y-%m-%d'))
    mydate += iter

    #pause the loop
    sleep(randint(1,3))

    # monitor requests
    serve += 1
    elapsed_time = time() - start_time

    # using bs4 to create variable to clean up site content

    soup = BeautifulSoup(r.text, 'html.parser')

    # establishing where data we are interested starts and ends

    chart = soup.find('table', {'class': 'chart-table'})

    tbody = chart.find('tbody')

    # empty array to be used for holding all variables we are scraping

    all_rows = []

    # actual scraping

    for tr in tbody.find_all('tr'):

        # scrape rank for each chart position

        rank_text = tr.find('td', {'class': 'chart-table-position'}).text

        # scrape artist name for each position and remove "by " so we only get artist name

        artist_text = tr.find('td', {'class': 'chart-table-track'}).find('span').text
        artist_text = artist_text.replace('by ','').strip()

        # scrape title of track for each position

        title_text = tr.find('td', {'class': 'chart-table-track'}).find('strong').text

        # scrape number of streams for each position
        streams_text = tr.find('td', {'class': 'chart-table-streams'}).text

        # do this to get program to start on first date 1/1/2019 instead of 1/2/2019
        date = (mydate - iter)

        # appending all variables we scraped to all_rows empty array and adding date to see exactly at which dates
        # program is failing to update skip variable, also for analysis for later when doing time series and regression
        all_rows.append( [rank_text, artist_text, title_text, streams_text, date.strftime('%Y-%m-%d')] )

    # create dataframe array to store all data

    df = pd.DataFrame(all_rows, columns =['Rank','Artist','Title','Streams', 'Date'])
    print(df)

    # writing csv file to output results
    with open('Spotify200chart.csv', 'a') as f:
        df.to_csv(f, header=False, index=False)
