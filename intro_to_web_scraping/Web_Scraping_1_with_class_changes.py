
# coding: utf-8

# ##Web Scraping 1: BeautifulSoup
# 
# [BeautifulSoup documentation](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
# 
# For Project Luther, we will be scraping information about movies from the internet. 

# ###Get the HTML from a page and convert to a BeautifulSoup object
# 
# we'll start by scraping some information from [this page](http://boxofficemojo.com/movies/?id=biglebowski.htm)

# In[1]:

import urllib2
from bs4 import BeautifulSoup

url = 'http://boxofficemojo.com/movies/?id=biglebowski.htm'

page = urllib2.urlopen(url)
soup = BeautifulSoup(page)



# In[2]:

print soup


# ##soup.find() 
# soup.find() is the most common function we will use from this package.  
# Let's try out some common variations of soup.find() 
# 

# In[3]:

# soup.find() returns the first match it finds. 
# search for a type of tag by using the tag as a string (like 'body','div','p','a') as an argument.
print soup.find('a')


# In[4]:

# soup.find_all() returns a list of all matches
for link in soup.find_all('a'): print link


# In[5]:

# you can match on an attribute like an id or class. 
print soup.find(class_='mp_box_content').find('table').attrs
print '\n'

#print soup.find(id='hp_footer')


# In[6]:

# retrieve the url from an anchor tag 
soup.find('a')['href']


# ##consistency
# Web scraping is made simple by the consistent format of information among like pages of a website.   
# 
# ### ok, enough chitchat.
# Let's choose some information to get about a movie and figure out how to get it with BeautifulSoup.

# ###items to scrape for each movie:
# * movie title
# * total domestic gross
# * release date
# * runtime
# * director
# * rating
# 

# In[7]:

# Movie Title
title_string = soup.find('title').text
title = title_string.split('(')[0].strip()
print title


# In[8]:

# Domestic Total Gross 
import re

dtg_string = soup.find(text=re.compile('Domestic Total Gross:'))
dtg = dtg_string.findNextSibling().text
dtg = dtg.replace('$','').replace(',','')
domestic_total_gross = int(dtg)

print domestic_total_gross
type(domestic_total_gross)


# In[9]:

# Release Date



# ###We can actually do several of these using the text matching method, so let's make a function for that
# 

# In[10]:

def get_movie_value(soup,value_name):
    '''
    takes a string attribute of a movie on the page and 
    returns the string in the next sibling object (the value for that attribute)
    '''
    obj = soup.find(text=re.compile(value_name))
    if not obj: 
        return None
    
    # this works for most of the values
    next_sibling = obj.findNextSibling()
    if next_sibling:
        return next_sibling.text

    # this next part works for the director
    elif obj.find_parent('td'):
        sibling_cell = obj.find_parent('td').findNextSibling()
        if sibling_cell:
            return sibling_cell.text
        
    else:
        return None
    
    


# In[11]:

# Let's get the following pieces of information using the function we just created

#release date
release_date = get_movie_value(soup,'Release Date:')
print release_date

#domestic total gross
dtg = get_movie_value(soup,'Domestic Total Gross:')
print dtg

#runtime
runtime = get_movie_value(soup,'Runtime')
print runtime

#rating
rating = get_movie_value(soup,'MPAA Rating')
print rating 

#director
director = get_movie_value(soup,'Director')
print director


# ###we need a few helper methods to parse the strings we've gotten

# In[12]:

import dateutil.parser

def to_date(datestring):
    date = dateutil.parser.parse(datestring)
    return date

def money_to_int(moneystring):
    moneystring = moneystring.replace('$','').replace(',','')
    return int(moneystring)

def runtime_to_minutes(runtimestring):
    runtime = runtimestring.split(' ')
    return int(runtime[0])*60 + int(runtime[2])


# In[13]:

#let's get these again and format them all in one swoop
rel_date = get_movie_value(soup,'Release Date')
print rel_date
release_date = to_date(rel_date)
domestic_total_gross = money_to_int(get_movie_value(soup,'Domestic Total Gross'))
runtime = runtime_to_minutes(get_movie_value(soup,'Runtime'))

headers = ['movie title','domestic total gross','release date','runtime (mins)','director','rating']

movie_data = []
movie_data.append(dict(zip(headers,[title,domestic_total_gross,release_date,runtime,director,rating])))

print movie_data


# In[14]:

a = ['a','b','c']
b = [1,2,3]

dict(zip(a,b))


# ###Now we need to generalize this so that we can take a url from boxofficemojo and create an entry in our movie data

# In[15]:

# adding the directory containing our python files to the path
import sys
sys.path.append('../movies/')

#import the module
import bomojo
bmj = bomojo.BOMojoScraper()

#create an empty list to start collecting the data
movie_data = []
movie_data.append(bmj.full_movie_dict_from_title("The Matrix"))
movie_data.append(bmj.full_movie_dict_from_title("The Sandlot"))
movie_data.append(bmj.full_movie_dict_from_title("Goonies"))

print movie_data



# ##To save the work for later, we can use pickle

# In[16]:

import pickle

with open('movie_data.pkl','wb') as outfile:
    pickle.dump(movie_data,outfile)


# In[17]:

#and checking to see that it is there
get_ipython().system(u'ls *.pkl')

