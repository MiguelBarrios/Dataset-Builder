from selenium import webdriver

class WebDriver:
    __instance = None
    @staticmethod
    def getInstance():
        if WebDriver.__instance == None:
            WebDriver()
        return WebDriver.__instance.driver
    def __init__(self):
        if WebDriver.__instance == None:
            self.driver = webdriver.Chrome('./chromedriver')
            WebDriver.__instance = self