number_of_new_articles = 5

import entry
from urllib2 import urlopen
import lxml.html
from lxml.cssselect import CSSSelector
import numpy as np
import pandas as pd
import re
import datetime

def get_page(url):
    try:
        html = urlopen(url).read()
        dom = lxml.html.fromstring(html)
        dom.make_links_absolute(url)
        return dom
    except:
        print 'Error'
        return None

def get_links_for_articles(main_page,headline_links_tag_list):
    for headline_links_tag in headline_links_tag_list:
        try:
            dom = get_page(main_page)
            sel = CSSSelector(headline_links_tag)
            res = sel(dom)
            hrefs = [e.get('href') for e in res]
            return [f for f in hrefs if f is not None]
        except:
            print 'Error'
            return None


def get_data_point(url,tag_list):
    for tag in tag_list:
        try:
            dom = get_page(url)
            sel = CSSSelector(tag)
            res = sel(dom)[0]
            return res.text
        except:
            print 'Error'
            return None



tags = pd.read_table('tags.txt', sep = ',')

results = pd.read_csv("Data.csv")


# Collect most recent stories
print results
print tags

i=1
urls = get_links_for_articles(tags.loc[i][1],[tags.loc[i][2],tags.loc[i][3]])[:number_of_new_articles]
index_to_write = results.shape[0]



j=1
headline = get_data_point(urls[j],[tags.loc[i][4],tags.loc[i][5]])
headline = re.sub('[^ A-Za-z0-9]', '', headline)
date = datetime.datetime.now()
new_row = [index_to_write,tags.loc[i][0],headline,date,urls[j],None,None]
results.loc[index_to_write] = new_row
results.to_csv("Data.csv")

print results

'''
for i in range(tags.shape[0]):
    urls = get_links_for_articles(tags.loc[i][1],[tags.loc[i][2],tags.loc[i][3]])[:number_of_new_articles]
    index_to_write = results.shape[0]
    for j in range(number_of_new_articles):
        headline = get_data_point(urls[j],[tags.loc[i][4],tags.loc[i][5]])
        headline = re.sub('[^ A-Za-z0-9]', '', headline)
        date = datetime.datetime.now()
        new_row = [index_to_write,tags.loc[i][0],headline,date,urls[j],None,None]
        results.loc[index_to_write] = new_row
        results.to_csv("Data.csv")

'''

# testing:

'''
main_page = 'https://www.theguardian.com/'
headline_links_tag = ['.js-headline-text']
headline_tag = ['.content__headline','.content__headline--immersive--with-main-media']
date_tag = ['time']


urls = get_links_for_articles(main_page,headline_links_tag)
print urls


url = urls[0]
date_tag1 = date_tag[0]

dom = get_page(url)
sel = CSSSelector(date_tag1)
res = sel(dom)
print res[0]
print res[0].text





'''
