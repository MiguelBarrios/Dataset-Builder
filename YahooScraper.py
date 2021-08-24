from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm
from util import *
import time
from util import * 
import random

class YahooScraper:
    def __init__(self, driver):
        self.search_engine_domain = 'https://yahoo.com'
        self.image_search_url = 'https://images.search.yahoo.com/'
        self.driver = driver
    def reset(self):
        self.driver.get(self.image_search_url)
    def run_search(self, search_query, n, output_dir):
        label = "serach request [search query:{}, n: {}, output directory: {}]"
        print(label.format(search_query, n, output_dir))
        self.reset()
        # get seach bar
        search_bar = self.driver.find_element_by_name("p")
        # Clear search bar
        search_bar.clear()
        # input seach request
        search_bar.send_keys(search_query)
        # press enter
        search_bar.send_keys(Keys.RETURN)
        # load all images from sear h
        self.load_all_results()
        image_links = self.find_n_images(output_dir, n)
    def find_n_images(self, output_dir, n):
        images = set()
        new_images = set()
        num_containers = 0
        html_doc = self.driver.find_element_by_xpath("//body").get_attribute('outerHTML')
        soup = BeautifulSoup(html_doc, 'html.parser')
        # get all image containers, excludes all yahoo icons
        containers = soup.find_all("li", {"class":"ld"})
        while len(containers) > num_containers:
            new_images.clear()
            num_containers = len(containers)
            for container in containers:
                image_container = container.find('img')
                if image_container != None:        
                    if image_container.has_attr('src'):
                        url = image_container['src']
                    else:
                        url = image_container['data-src']
                    if url != None and url not in images:
                        new_images.add(url)
            # download new images
            if len(new_images) + len(images) < n:
                save_images(new_images, output_dir)
            else:
                res = n - len(images)
                save_images(random.sample(new_images, res), output_dir)                
            images.update(new_images)
            if len(images) > n:
                return images
            html_doc = self.driver.find_element_by_xpath("//body").get_attribute('outerHTML')
            soup = BeautifulSoup(html_doc, 'html.parser')
            # get all image containers, excludes all yahoo icons
            containers = soup.find_all("li", {"class":"ld"})
        return images
    def load_all_results(self):
        print("loading results.", end = "")
        while True:    
            try:
                load_more_btn = self.driver.find_element_by_name('more-res')
                load_more_btn.click()
                print(".", end = "")
            except Exception as e:
                break
        print(" FINISHED")
