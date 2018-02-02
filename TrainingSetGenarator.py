
from Scraper import Scraper
import json

def compile_reviews(review_text, review_stars):
    """ Complie a dictionary of the review's text, review's stars and lable the
        review as poitive or negative
    Args:
        review_text (list): text of the reviews
        review_stars (list): star rating of the reviews
    Returns:
        reviews (list): list of all the complied reviews
    """
    
    reviews = list()
    for t,s in zip(review_text, review_stars):
        review_dict = dict()
        review_dict["text"] = t.text.encode("ascii","ignore").decode()
        review_dict["stars"] = int(s.text.encode("ascii","ignore").decode()[0])
        if review_dict["stars"] <= 2:
            review_dict["label"] = "negative"
        elif review_dict["stars"] >= 4:
            review_dict["label"] = "positive"
        else:
            continue
        reviews.append(review_dict)
    return reviews

def get_reviews(url):
    """ Scrape reviews off each review page
    Args:
        url (str): url of the product page
    Returns:
        reviews (list): list of all the scraped reviews
    """
    
    scraper = Scraper()
    review_url = scraper.get_reviews_page(url)
    soup = scraper.get_soup(review_url)
    lastPage = scraper.get_last_page(soup)
    reviews = list()
    for i in range(1, lastPage + 1):
        soup = scraper.get_soup(review_url + "&pageNumber=" + str(i))
        review_stars = soup.find_all(attrs={"data-hook": "review-star-rating"})
        review_text = soup.find_all("span",'a-size-base review-text')
        reviews += compile_reviews(review_text, review_stars)
    return reviews

def save_to_json(reviews):
    """ Save the reviews to data.json file
    Args:
        reviews (list): list of all the scraped reviews
    """
    
    with open ("data.json", "w") as jf:
        for review in reviews:
            json.dump(review, jf, sort_keys=True, indent=4)

if __name__ == "__main__":
    asin = "B073QVY9PQ"
    url = "https://www.amazon.in/dp/" + asin
    reviews = get_reviews(url)
    save_to_json(reviews)
    

