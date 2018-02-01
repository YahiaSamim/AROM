
from Scraper import Scraper

if __name__ == "__main__":
    asin = "B073QVY9PQ"
    url = "https://www.amazon.in/dp/" + asin
    scraper = Scraper()
    reviews = scraper.get_reviews(url)
    for review in reviews:
        print(review)
