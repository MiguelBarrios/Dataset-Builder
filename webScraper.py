from YahooScraper import *
from pinterestScraper import *
from unsplashScraper import *

class WebScraper:
    def __init__(self, search_yahoo = True, search_pinterest = True, search_unsplash = True):
        self.yahooScraper = YahooScraper() if search_yahoo else None
        self.pinterestScraper = PinterestScraper() if search_pinterest else None
        self.unsplashScraper = UnsplashScraper() if search_unsplash else None
    def run_search(self, search_query, n, output_dir):
        label = "search request [search query:{}, n: {}, output directory: {}]"
        print(label.format(search_query, n, output_dir))
        if self.yahooScraper != None:
            self.yahooScraper.run_search(search_query, n, output_dir)
        if self.pinterestScraper != None:
            self.pinterestScraper.run_search(search_query, n, output_dir)
        if self.unsplashScraper != None:
            self.unsplashScraper.run_search(search_query, n, output_dir)        
    def run_multiple_searches(self, search_queries, n, parent_dir):
        if self.yahooScraper != None:
            self.__run_searches(self.yahooScraper, search_queries, n, output_dir)
        if self.pinterestScraper != None:
            self.__run_searches(self.pinterestScraper, search_queries, n, output_dir)
        if self.unsplashScraper != None:
            self.__run_searches(self.unsplashScraper, search_queries, n, output_dir)
    def __run_searches(self, scraper, search_queries, n, parent_dir):
        for search_query in search_queries:
            output_dir = parent_dir + search_query
            scraper.run_search(search_query, n, output_dir)
        