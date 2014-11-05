from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

chrome = webdriver.Chrome('/Users/Home/Packages/chromedriver')

matrix_url = "http://www.imdb.com/"
chrome.get(matrix_url)

search_director = chrome.find_element_by_id('navbar-query')
search_director.send_keys("Martin Scorsese")
search_director.send_keys(Keys.RETURN)

click_director = chrome.find_element_by_link_text('Martin Scorsese')
click_director.send_keys(Keys.RETURN)

award_director = chrome.find_element_by_css_selector('div.article.highlighted')
award_information = award_director.text
award_information = award_information.replace('.','').replace('wins','win').replace('Oscars','Oscar').replace('nominations','nomination')
award_information_list = award_information.split()

print award_information_list

if "Oscar" in award_information:
    oscar_index = award_information_list.index('Oscar')
    oscar_index_value = oscar_index - 1
    num_of_oscar = award_information_list[oscar_index_value]
print num_of_oscar, "Oscar"

if "win" in award_information:
    win_index = award_information_list.index('win')
    win_index_value = win_index - 1
    num_of_win = award_information_list[win_index_value]
print num_of_win, "win"

if "nominations" or "nominations" in award_information:
    nomination_index = award_information_list.index('nomination')
    nomination_index_value = nomination_index - 1
    num_of_nomination = award_information_list[nomination_index_value]
print num_of_nomination, "nomination"