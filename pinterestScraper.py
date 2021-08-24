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

class PinterestScraper:
    def __init__(self):
        self.domain = 'https://www.pinterest.com/'
        self.driver = WebDriver.getInstance()
        self.load_home_page()
        self.log_in()
    def run_search(self, search_query, n, output_dir):
        images_found = self.run_search_query(search_query, n)
        num_images_saved = save_images(images_found, output_dir)
        return num_images_saved
    def load_home_page(self):
        self.driver.get(self.domain)
    def log_in(self):
        # click on log in button
        log_in = self.driver.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[1]/div[1]/div[2]/div[2]/button/div')
        log_in.click()
        # Enter userName and password
        username_input = self.driver.find_element_by_name("id")
        password_input = self.driver.find_element_by_name("password")
        username_input.send_keys(config.USERNAME_PINTEREST)
        password_input.send_keys(config.PASSWORD_PINTEREST)
        # click log in button
        log_in_button = self.driver.find_element_by_class_name('SignupButton')
        log_in_button.click()
    def run_search_query(self, search_query, n, load_time = 1):
        search_bar = self.driver.find_element_by_name('searchBoxInput')
        self.clear_search_bar(search_bar)
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.RETURN)
        images = self.find_n_images(n)
        return images
    #.clear() did not work
    def clear_search_bar(self, search_bar):
        while len(search_bar.get_attribute('value')) > 0:
            # create action chain object
            action = ActionChains(self.driver)
            # double click the item
            action.double_click(on_element = search_bar)
            action.perform()
            search_bar.send_keys(Keys.DELETE)
    def find_n_images(self, n):
        images = set()
        images_found = 0
        load_time = 1
        last_hight = 0
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        while images_found < n and last_hight != new_height:
            html_doc = self.driver.find_element_by_xpath("//body").get_attribute('outerHTML')
            soup = BeautifulSoup(html_doc, 'html.parser')
            get_links(soup, images)
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(load_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            last_height = new_height
            images_found = len(images)
            print("images found: {}".format(images_found), end = '\r')
        return images
