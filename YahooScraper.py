from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm
from util import *
import time
from selenium import webdriver

class YahooScraper:
	def __init__(self):
		self.search_engine_domain = 'https://yahoo.com'
		self.image_search_url = 'https://images.search.yahoo.com/'
		self.images_found = 1

	def run_search_request(self, driver, search_query):
		driver.get(self.image_search_url)
		# get seach bar
		search_bar = driver.find_element_by_name("p")
		# Clear search bar
		search_bar.clear()
		# input seach request
		search_bar.send_keys(search_query)
		# press enter
		search_bar.send_keys(Keys.RETURN)

	def search_and_save(self, driver, search_query, output_directory):
		self.run_search_request(driver, search_query)
		# get current page html
		self.load_all_results(driver)
		html_doc = driver.find_element_by_xpath("//body").get_attribute('outerHTML')
		soup = BeautifulSoup(html_doc, 'html.parser')
		# get all image containers
		#containers = soup.find_all('li')
		containers = soup.find_all("li", {"class":"ld"})
		for container in containers:
			image_container = container.find('img')
			if image_container != None:        
				if image_container.has_attr('src'):
					# working
					url = image_container['src']
					#print(image_container['src'])
				else:
					url = image_container['data-src']
				if url != None:
					file_name = "{}/{}.png".format(output_directory, self.images_found)
					if download_image(url, file_name, output_directory):
						self.images_found = self.images_found + 1
	# TODO: find way to do without try catch
	def load_all_results(self, driver):
		print("loading.", end = "")
		while True:    
			try:
				load_more_btn = driver.find_element_by_name('more-res')
				load_more_btn.click()
				print(".", end = "")
			except:
				break
		print("\nFinished")


"""

def page_has_loaded(driver, sleep_time = 2):
    '''
    Waits for page to completely load by comparing current page hash values.
    '''
    def get_page_hash(driver):
        '''
        Returns html dom hash
        '''
        # can find element by either 'html' tag or by the html 'root' id
        dom = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
        # dom = driver.find_element_by_id('root').get_attribute('innerHTML')
        dom_hash = hash(dom.encode('utf-8'))
        return dom_hash

    page_hash = 'empty'
    page_hash_new = ''
    # comparing old and new page DOM hash together to verify the page is fully loaded
    while page_hash != page_hash_new: 
        page_hash = get_page_hash(driver)
        time.sleep(sleep_time)
        page_hash_new = get_page_hash(driver)
        print('<page_has_loaded> - page not loaded')

    print('<page_has_loaded> - page loaded: {}'.format(driver.current_url))

"""









