# works with Microsoft Edge and it's driver
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from bs4 import BeautifulSoup


def open_driver():
    """
    Open and return driver.
    
    Note : Path t0 Chrome driver should be set correctly.
    """
    driver_path = r"C:\Users\user\Downloads\Softwares\chromedriver_win32\chromedriver.exe"
    return webdriver.Chrome(driver_path)


def load_url(driver : WebDriver,
             url : str,
             verbose : int = 0):
    """
    Load URL using driver.
    
    Parameters
    ----------
    driver : selenium.chrome.webdriver.
    
    url : str.
    
    verbose : boolean, default=False
        if True, print function log.
    """
    if verbose >= 5: print("Loading page")
    try:
        driver.get(url) # loading page
    except Exception as e:
        print(f"Failed loading page, exception : {e}")
        
        
def get_driver_page_source(driver : WebDriver):
    """Extract page source and return BeautifulSoup object."""
    return BeautifulSoup(driver.page_source, "lxml")
