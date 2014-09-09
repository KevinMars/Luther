import csv 
import urllib2
import re
import sys
from bs4 import BeautifulSoup

url = 'http://boxofficemojo.com/yearly/chart/?yr=1997&p=.htm'

page = urllib2.urlopen(url)
soup = BeautifulSoup(page)

base_url = 'http://boxofficemojo.com'
movie_urls = []
for incomplete_url in soup.find_all(href=re.compile("movies")):        
    if "movies/?id" in incomplete_url['href']:
        incomplete_url = str(incomplete_url['href'])
        movie_urls.append(base_url+incomplete_url)



sys.path.append('../movies/')

#import the module
import bomojo
bmj = bomojo.BOMojoScraper()

movie_dict = []
for x in movie_urls:
    try:
        movie_dict.append(bmj.parse_full_mojo_page(x))      
    except:
        pass       
print movie_dict

first_movie_dict = movie_dict[0]
movie_keys = list(first_movie_dict.keys())


open_file = open('movies.csv', 'w')
dict_writer = csv.DictWriter(open_file,movie_keys)
dict_writer.writer.writerow(movie_keys)
dict_writer.writerows(movie_dict)


