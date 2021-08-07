from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from DogPileScraper import *
import os

class Scraper:
	def __init__(self, search_engine):
		self.driver = webdriver.Chrome('./chromedriver')
		self.search_engine = self.get_search_engine(search_engine)
	#
	def get_search_engine(self, search_engine):
		if(search_engine == 'Google'):
			return GoogleScraper()
		elif search_engine == 'Dogpile':
			return DogPileScraper()
		elif search_engine == 'Yahoo':
			return YahooScraper()
		elif search_engine == 'Bing':
			return BingScraper()
		elif search_engine == 'DuckDuckGo':
			return DuckDuckGoScraper()
	#
	def seach_and_save(self, search_query, output_directory):
		# create directory if not present
		if not os.path.exists(output_directory):
			os.makedirs(output_directory)

		images_found = self.search_engine.find_image_links(self.driver, search_query, output_directory)
		print(images_found)