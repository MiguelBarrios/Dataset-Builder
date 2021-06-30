from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm

class ImgScraper:
	def __init__(self):
		self.driver = webdriver.Chrome('./chromedriver')
		self.search_engine_domain = 'https://www.dogpile.com/'
		self.initial_search_url = 'https://www.dogpile.com/?sc=AMEEaIMj9a8o00'
		self.image_links = []
	# --------
	def seach_and_save_images(self, search_request, number_images_to_download, output_directory):
		# create directory if not present
		if not os.path.exists(output_directory):
			os.makedirs(output_directory)
		# clear image list
		self.image_links.clear()
		# Open website in Chrome
		self.driver.get(self.initial_search_url)
		# get seach bar
		search_bar = self.driver.find_element_by_name("q")
		# Clear search bar
		search_bar.clear()
		# input seach request
		search_bar.send_keys(search_request)
		# press enter
		search_bar.send_keys(Keys.RETURN)
		# get current page html
		html_doc = self.driver.find_element_by_xpath("//body").get_attribute('outerHTML')
		soup = BeautifulSoup(html_doc, 'html.parser')
		# get all image containers
		img_containers = soup.find_all("div",{"class":"image"})
		# Extract link for each image in page
		for container in img_containers:
			a = container.find('img')
			img_url = a['src']
			self.image_links.append(img_url)
			# Scrape images until required amount is reached
			while(len(self.image_links) < number_images_to_download):
				try: 
					next_container = soup.find("a", {"class": "pagination__num--next"})
					next_page_link = self.search_engine_domain + next_container['href']
				except:
					## Last page of results
					print("No more images Avaliable")
					break
				# open next page of images
				self.driver.get(next_page_link)
				html_doc = self.driver.find_element_by_xpath("//body").get_attribute('outerHTML')
				soup = BeautifulSoup(html_doc, 'html.parser')
				img_containers = soup.find_all("div",{"class":"image"})
				for container in img_containers:
					a = container.find('img')
					link = a['src']
					self.image_links.append(link)
				print("Images found: " + str(len(self.image_links)))
		ImgScraper.save_images(self.image_links, output_directory)
	#--------------------------
	def save_images(img_links, output_directory):
		print("Saving images")
		count = 1
		for url in tqdm(img_links):
			file_name = "{}/{}.png".format(output_directory,count)
			try:
				ImgScraper.download_image_from_link(file_name, url)
				count = count + 1
			except:
				print("Invalid img Link: " + url)
	#--------------------------
	def download_image_from_link(file_name, url):
		response = requests.get(url)
		file = open(file_name, "wb")
		file.write(response.content)
		file.close()

if __name__ == "__main__":
	scraper = ImgScraper()
	search_request = "mountains"
	output_dir = "mountains"
	min_number_images_to_download = 500
	scraper.seach_and_save_images(search_request, min_number_images_to_download, output_dir)

