from bs4 import BeautifulSoup
from selenium.webdriver.edge.webdriver import WebDriver
from typing import Dict
from time import sleep
from random import randint
from edge_driver import (load_url, 
                         get_driver_page_source)

REVIEW_PAGE_URL_IDENTIFIER = ["product-reviews", 
                              "ref=cm_cr_getr_d_paging_btm_next", 
                              "&pageNumber"]

REVIEW_PAGE_NO_URL_IDENTIFIER = ["cm_cr_getr_d_paging_btm_next_", 
                                 "&pageNumber="]

def extract_profile_id(profile_link : str):
    """
    Extract and return profile id from profile_link.
    
    Paramters
    ---------
    profile_link : str.
    
    Returns
    -------
    profile_id : str.
    """
    default_start = "/gp/profile/amzn1.account."
    default_end = "/ref=cm_cr_arp_d_gw_btm?ie=UTF8"
    return profile_link[len(
        default_start
    ):profile_link.find(default_end)]


def extract_page_reviews(
    page_source_soup : BeautifulSoup):
    """
    Extract reviews from the Amazon review page.
    
    Parameters
    ----------
    page_source_soup : bs4.BeautifulSoup.
    
    Returns
    -------
    review : Dict.
    """
    reviews = page_source_soup.find_all(name="div", attrs={"data-hook":"review"})
    contents = {}
    for i, review in enumerate(reviews):
        try:
            content = {}
            profile = review.find(name="a", attrs={"class":"a-profile"})["href"]
            name = review.find(name="span", attrs={"class":"a-profile-name"}).text
            rating = review.find(name="a", attrs={"class":"a-link-normal"})["title"]
            title = review.find(name="a", attrs={"data-hook":"review-title"}).text
            date = review.find(name="span", attrs={"data-hook":"review-date"}).text
            body = review.find(name="span", attrs={"data-hook":"review-body"})
            helpful_count = review.find(name="span", attrs={"data-hook":"helpful-vote-statement"})
            images = review.find(name="div", attrs={"class":"review-image-tile-section"})
            content["name"] = name
            content["rating"] = rating
            content["title"] = title
            content["date"] = date
            content["helpful_count"] = helpful_count
            content["body"] = body
            content["images"] = images
            contents[extract_profile_id(profile)] = content
        except Exception as e:
            print(f"Failed review extraction from page source, exception : {e}")
    return contents

def is_review_page_url(url : str) -> bool:
    """Return True if Amazon verified customers review page."""
    for identifier in REVIEW_PAGE_URL_IDENTIFIER:
        if identifier not in url:
            return False
    return True

def get_review_page_number_from_url(url : str) -> int:
    """Return review page number from the URL."""
    return int(
        url[url.find(
            REVIEW_PAGE_NO_URL_IDENTIFIER[1]
        ) + len(REVIEW_PAGE_NO_URL_IDENTIFIER[1]):]
    ) 

def update_review_url_for_page_no(url : str, 
                                  page_no : int) -> str:
    """Update and return review page number URL for input page number."""
    old_page_no = get_review_page_number_from_url(url)
    for identifier in REVIEW_PAGE_NO_URL_IDENTIFIER:
        url = url.replace(f"{identifier}{old_page_no}", 
                          f"{identifier}{page_no}")
    return url

def extract_all_reviews(driver : WebDriver,
                        url : str,
                        start_page_no : int= 1,
                        max_num_pages: int= 500, 
                        verbose: int = 0) -> Dict:
    """Extract reviews for first 500 available review pages."""
    success_page_nos = []
    failed_page_nos = []
    reviews = {}
    
    if not is_review_page_url(url):
        return
    
    for page_no in range(start_page_no, max_num_pages+1):
        if verbose >= 1: print(f"Extracting reviews from page : {page_no}")
        page_url = update_review_url_for_page_no(url, page_no)
        
        # loading review page
        try:
            load_url(driver=driver, url=page_url, verbose=verbose)
            sleep(randint(5,10))
        except Exception as e:
            failed_page_nos.append(page_no)
            print(f"Failed loading page, exception : {e}")
            continue # skip this page
        
        # extracting reviews from page
        try:
            page_source = get_driver_page_source(driver)
            reviews[page_no] = extract_page_reviews(page_source)
        except Exception as e:
            failed_page_nos.append(page_no)
            print(f"Failed extfracting reviews, exception : {e}")
            continue # skip this page
    return reviews   a
a

