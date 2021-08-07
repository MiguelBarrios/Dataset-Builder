from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm

class DogPileScraper:
	def __init__(self):
		self.search_engine_domain = 'https://www.dogpile.com/'
		self.image_search_url = 'https://www.dogpile.com/?qc=images'
		self.images_found = 1

	def run_search_request(self, driver, search_query):
		driver.get(self.image_search_url)
		# get seach bar
		search_bar = driver.find_element_by_name("q")
		# Clear search bar
		search_bar.clear()
		# input seach request
		search_bar.send_keys(search_query)
		# press enter
		search_bar.send_keys(Keys.RETURN)

	def find_image_links(self, driver, search_query, output_directory):
		images = []
		self.run_search_request(driver, search_query)
		# get current page html
		html_doc = driver.find_element_by_xpath("//body").get_attribute('outerHTML')
		soup = BeautifulSoup(html_doc, 'html.parser')
		# get all image containers
		img_containers = soup.find_all("div",{"class":"image"})
		# Extract link for each image in page
		for container in img_containers:
			a = container.find('img')
			image_url = a['src']
			file_name = "{}/{}.png".format(output_directory, self.images_found)
			print(file_name)

		available =  True
		while(available):
			available =  self.load_next_page(driver, soup)
			html_doc = driver.find_element_by_xpath("//body").get_attribute('outerHTML')
			soup = BeautifulSoup(html_doc, 'html.parser')
			# get all image containers
			img_containers = soup.find_all("div",{"class":"image"})
			# Extract link for each image in page
			for container in img_containers:
				a = container.find('img')
				image_url = a['src']
				file_name = "{}/{}.png".format(output_directory, self.images_found)
				if save_image(image_url, file_name, output_directory):
					self.images_found = self.images_found + 1
			available = self.load_next_page(driver, soup)
		return self.images_found
	def load_next_page(self, driver, soup):
		try: 
			next_container = soup.find("a", {"class": "pagination__num--next"})
			next_page_link = self.search_engine_domain + next_container['href']
			driver.get(next_page_link)
			return True
		except Exception as e: 
			print(e)
			currentURL = driver.title
			print("currentUrl: {}".format(currentURL))
			recapture_complete = input('recapture complete: ["yes", "no"]\n')
			if recapture_complete == 'yes':
				next_container = soup.find("a", {"class": "pagination__num--next"})
				next_page_link = self.search_engine_domain + next_container['href']
				driver.get(next_page_link)
				return True
			return False

def save_image(image_url, file_name, output_directory):
	try:
		response = requests.get(image_url)
		file = open(file_name, "wb")
		file.write(response.content)
		file.close()
		print("image saved at {}".format(image_url))
		return True
	except Exception as e:
		#print("invalid link: {}".format(image_url))
		#print(e)
		return False


"""
class GoogleScraper:
	def __init__(self):
		self.image_search_url = 'https://www.google.com/imghp?hl=en'

class DogPileScraper:
	def __init__(self):
		self.image_search_url = 'https://www.dogpile.com/?qc=images'

class YahooScraper:
	def __init__(self):
		self.image_search_url = 'https://images.search.yahoo.com/'

class BingScraper:
	def __init__(self):
		self.image_search_url = 'https://www.bing.com/images/trending?FORM=ILPTRD'

# different
class DuckDuckGoScraper:
	def __init__(self):
		self.image_search_url = 'https://www.bing.com/images/trending?FORM=ILPTRD'
"""