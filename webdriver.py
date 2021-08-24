from selenium import webdriver

class WebDriver:
    __instance = None
    @staticmethod
    def getInstance():
        if WebDriver.__instance == None:
            WebDriver()
        return WebDriver.__instance.driver
    @staticmethod
    def toggle_log_in_flag():
        WebDriver.__instance.logged_in = True
    @staticmethod
    def logged_in():
        if WebDriver.__instance == None:
            return False
        return WebDriver.__instance.logged_in

    def __init__(self):
        if WebDriver.__instance == None:
            self.driver = webdriver.Chrome('./chromedriver')
            self.logged_in = False
            WebDriver.__instance = self