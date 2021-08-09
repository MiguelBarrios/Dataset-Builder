from scraper import *
import os

if __name__ == "__main__":
	#scraper = Scraper('Dogpile')
	#scraper.seach_and_save('mountains', 'mountainImages')
	scraper = Scraper('Yahoo')
	scraper.search_and_save('dogs', 'outputDir')


