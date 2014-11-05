
# coding: utf-8

# ### What happens if I try to parse my gmail with urllib and BeautifulSoup?

# We have hit the login page. We can't get to the emails without logging in. Again, reading the html source is useless, because it is only the source for the login page.

# ### Open chrome, go to gmail, log in to Irmak's hacking account, compose an email, send it

# In[4]:

# pip install selenium
# Download ChromeDriver from https://code.google.com/p/selenium/wiki/ChromeDriver

# Documentation on finding elements:
#http://selenium-python.readthedocs.org/en/latest/locating-elements.html
# Xpath tutorial:
# http://www.w3schools.com/xpath/xpath_syntax.asp

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# in case your computer complains about the driver even though it's there
# import os
# os.environ


# ### Scraping boxofficemojo with selenium

# In[8]:

chrome = webdriver.Chrome('/Users/Home/Packages/chromedriver')

matrix_url = "http://www.imdb.com/"
chrome.get(matrix_url)


# In[9]:

search_director = chrome.find_element_by_id('navbar-query')
search_director.send_keys("Martin Scorsese")
search_director.send_keys(Keys.RETURN)


# In[10]:

click_director = chrome.find_element_by_link_text('Martin Scorsese')
click_director.send_keys(Keys.RETURN)


# In[11]:

award_director = chrome.find_element_by_css_selector('div.article.highlighted')
award_information = award_director.text
award_information = award_information.replace('.','').replace('wins','win').replace('Oscars','Oscar').replace('nominations','nomination')
award_information_list = award_information.split()

print award_information_list


# In[ ]:

if "Oscar" in award_information:
    oscar_index = award_information_list.index('Oscar')
    oscar_index_value = oscar_index - 1
    num_of_oscar = award_information_list[oscar_index_value]
print num_of_oscar


# In[ ]:

if "win" in award_information:
    win_index = award_information_list.index('win')
    win_index_value = win_index - 1
    num_of_win = award_information_list[win_index_value]
print num_of_win


# In[ ]:

if "nominations" or "nominations" in award_information:
    nomination_index = award_information_list.index('nomination')
    nomination_index_value = nomination_index - 1
    num_of_nomination = award_information_list[nomination_index_value]
print num_of_nomination


# In[ ]:

chrome.close()

