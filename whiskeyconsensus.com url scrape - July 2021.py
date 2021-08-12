#!/usr/bin/env python
# coding: utf-8


# load libraries
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


# grab the webpage that contains all of the URLs for the review pages
url = 'https://whiskeyconsensus.com/reviews/'

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
}

page = requests.get(url, headers=header)

soup = BeautifulSoup(page.content, 'html.parser')


# parse the webpage to extract the url for each review
results = soup.find_all('div', class_ = 'wppr-post-title wppr-col')

urlList = []

for urls in results:
    link = urls.find('a')['href']
    urlList.append(link)
    
datUrl = pd.DataFrame(urlList, columns =['reviewUrl'])


# Export data
datUrl.to_pickle("./whiskeyconsensus-reviews-urls.pkl")
