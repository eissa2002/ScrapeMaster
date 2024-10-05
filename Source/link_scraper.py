from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class WebsiteLinkScraper:
    def __init__(self, driver_path, chrome_options=None):
        """Initialize the link scraper."""
        self.driver_path = driver_path
        self.chrome_options = chrome_options if chrome_options else Options()

    def search_for_websites(self, query, num_results=30):
        """Search for websites using Google."""
        driver = webdriver.Chrome(service=Service(self.driver_path), options=self.chrome_options)
        driver.get("https://www.google.com")

        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        results = driver.find_elements(By.CSS_SELECTOR, 'div.yuRUbf a')
        websites = [result.get_attribute('href') for result in results[:num_results]]

        driver.quit()
        return websites
