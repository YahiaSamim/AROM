from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import requests
from bs4 import BeautifulSoup

class Scraper:

    def __init__(self):
        """
            Default constructor
        """
        
        pass
    
    def get_reviews_page(self, url):
        """ Navigate to the all reviews page
        Agrs:
            url (str): url of the the product page
        Returns:
            review_url (str): url of the all reviews page
        """
        
        chromeOptions = Options()  
        chromeOptions.add_argument("--headless")
        driverPath = "C:/Users/User/AppData/Local/Programs/Python/Python36-32/AROM/chromedriver"
        driver = webdriver.Chrome(driverPath, chrome_options = chromeOptions)
        driver.get(url)
        driver.find_element_by_xpath("""//*[@id="reviews-medley-footer"]/div[1]/a""").click()
        driver.switch_to_window(driver.window_handles[-1])
        review_url = driver.current_url
        driver.close()
        return review_url

    def get_soup(self, url):
        """ Create soup object of the url
        Args:
            url (str): url to create the soup object
        Returns:
            soup (soup): soup object
        """
        
        request = requests.get(url)
        soup = BeautifulSoup(request.text, "html.parser")
        return soup

    def get_last_page(self, soup):
        """ Get the last review page number
        Args:
            soup (soup): soup object
        returns:
            lastPage (int): last review page number
        """
        
        pageNumber = []
        reviewNumber = int(soup.find("span", "a-size-medium totalReviewCount").text.replace(',', ''))
        if reviewNumber <= 10:
            lastPage = 1
        else:
            for link in soup.find_all(attrs={"class": "page-button"}):
                pageNumber.append(link.get_text())
                lastPage1 = pageNumber[len(pageNumber)-1]
                lastPage = int(lastPage1) 
        return lastPage

    def get_reviews(self, url):
        """ Scrape reviews off each review page
        Args:
            url (str): url of the product page
        Returns:
            reviews (list): list of all the scraped reviews
        """
        
        review_url = self.get_reviews_page(url)
        soup = self.get_soup(review_url)
        lastPage = self.get_last_page(soup)
        reviews = list()
        for i in range(1, lastPage + 1):
            soup = self.get_soup(review_url + "&pageNumber=" + str(i))
            review_text = soup.find_all("span",'a-size-base review-text')
            for t in review_text:
                reviews.append(t.text.encode("ascii","ignore").decode())
        return reviews

