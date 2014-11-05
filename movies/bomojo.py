import sys
import re
import urllib2
import scraper
from bs4 import BeautifulSoup
import dateutil.parser
import urlparse

class BOMojoScraper(scraper.Scraper):

    base_url = "http://www.boxofficemojo.com/"
    search_url = base_url + "search/?q=%s"

    def full_movie_dict_from_title(self,movie_name):
        return self.parse_full_mojo_page(self.get_full_page_url_from_title(movie_name))

    def get_full_page_url_from_title(self,movie_name):
        search_soup = self.search(movie_name)
        found_matches = search_soup.find(text=re.compile("Movie Matches"))
        if found_matches:
            matches_table = found_matches.parent.find_next_sibling("table")
            result_row = matches_table.find_all('tr')[1]
            full_page_url = urlparse.urljoin(self.base_url,result_row.find('a')['href'])

            return full_page_url

        # if we end up here without returning anything, we did not hit a match
        log_message = "[LOG: No match found for %s]" % movie_name
        print >> sys.stderr, log_message
        return -1


    def parse_full_mojo_page(self,full_page_url):
        soup = self.connect(full_page_url)

        release_date = self.to_date(
            self.get_movie_value(soup,'Release Date'))
        domestic_total_gross = self.money_to_int(
            self.get_movie_value(soup,'Domestic Total Gross'))
        runtime = self.runtime_to_minutes(self.get_movie_value(soup,'Runtime'))
        director = self.get_movie_value(soup,'Director')
        rating = self.get_movie_value(soup,'MPAA Rating')
        budget = self.budget_to_int(self.get_movie_value(soup,'Production Budget'))
        openingweekendgross = self.opening_weekend_gross_to_int(self.get_movie_value(soup, 'Opening\xa0Weekend:'))

        movie_dict = {
            'movie_title':self.get_movie_title(soup),
            'release_date':release_date,
            'domestic_total_gross':domestic_total_gross,
            'runtime':runtime,
            'director':director,
            'rating':rating,
            'budget':budget,
            'openingweekendgross':openingweekendgross
        }

        return movie_dict
            

    def get_movie_value(self,soup,value_name):
        '''
        takes a string attribute of a movie on the page and 
        returns the string in the next sibling object (the value for that attribute)
        '''
        obj = soup.find(text=re.compile(value_name))
        
        if not obj: 
            return None
    	
    	if "Opening\xa0Weekend" in value_name and u"Limited" in obj:
    		obj = soup.find(text=re.compile('Wide\xa0Opening\xa0Weekend:'))
        
        # this works for most of the values
        next_sibling = obj.findNextSibling()
        
        
        if next_sibling:
            return next_sibling.text

        # this next part works for the director
        elif obj.find_parent('tr'):
            sibling_cell = obj.find_parent('td').findNext('td')
            if sibling_cell:
                return sibling_cell.text
        
        else:
    		return -1

    def get_movie_title(self,soup):
        title_tag = soup.find('title')
        movie_title = title_tag.text.split('(')[0].strip()
        return movie_title
    
    def to_date(self,datestring):
        return dateutil.parser.parse(datestring)

    def money_to_int(self,moneystring):
        return int(moneystring.replace('$','').replace(',',''))

    def runtime_to_minutes(self,runtimestring):
        rt = runtimestring.split(' ')
        return int(rt[0])*60 + int(rt[2])
        
    def budget_to_int(self,budgetstring):
		if "N/A" in budgetstring:
			pass
		else:
			budgetstring = budgetstring.replace('$','')
			if "million" in budgetstring:
				budgetstring = budgetstring.replace(' ','')
				if "." in budgetstring:
					budgetstring = budgetstring.replace ('.','').replace('million','00000')
				else:
					budgetstring = budgetstring.replace('million','000000')
			else:
				budgetstring = budgetstring.replace(',','')
			return int(budgetstring)
			
    def opening_weekend_gross_to_int(self,weekendmoneystring):
    	try:
    		return int(weekendmoneystring.replace('$','').replace(',',''))
    	except:
			pass
		
	
    			
    		    	
