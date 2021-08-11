from scraper import *
from pinterestScraper import *
import time

if __name__ == "__main__":

	#Scrapers: ['Yahoo, Pintrest']
	#scraper = Scraper('Dogpile')
	#scraper.seach_and_save('mountains', 'mountainImages')

	### Pinterest test
	driver = webdriver.Chrome('./chromedriver')
	scraper = PinterestScraper(driver)
	print("waiting")
	time.sleep(5)
	scraper.run_search("yellow bird", 25, 'yellowBirds')
	scraper.run_search("red bird", 25, 'redBirds')



