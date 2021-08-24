from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import time
import re
from config import *
from util import *
import os, os.path
from webdriver import *

class UnsplashScraper:
    def __init__(self):
        self.domain = 'https://unsplash.com/'
        self.driver = WebDriver.getInstance()

    def run_search(self, search_query, n, output_dir):
        print("Scraping Unsplash")
        # load home page
        self.driver.get(self.domain)
        # clear search bar and enter search query
        search_bar = self.driver.find_element_by_name('searchKeyword')
        clear(search_bar, self.driver)
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(4)
        # scrape images
        images_found = self.find_n_images(n)
        num_images_saved = save_images(images_found, output_dir)
        return num_images_saved
    def find_n_images(self, n):
        images = set()
        images_found = 0
        load_time = 1
        last_hight = 0
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        while images_found < n and last_hight != new_height:
            html_doc = self.driver.find_element_by_xpath("//body").get_attribute('outerHTML')
            soup = BeautifulSoup(html_doc, 'html.parser')
            new_images = soup.find_all('img')
            for i in new_images:
                img_url = i['src']
                if valid_img(img_url):
                    images.add(img_url)
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(load_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            last_height = new_height
            images_found = len(images)
            print("images found: {}".format(images_found), end = '\r')
        return images
