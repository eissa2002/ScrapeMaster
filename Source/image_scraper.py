import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils import scroll_down

class ImageScraper:
    def __init__(self, driver_path, chrome_options=None):
        """Initialize the image scraper."""
        self.driver_path = driver_path
        self.chrome_options = chrome_options if chrome_options else Options()

    def download_image(self, img_url, save_folder, log_file):
        """Download an image from a URL and log the result."""
        try:
            img_data = requests.get(img_url).content
            if len(img_data) < 1024:  # Skip small images (< 1KB)
                print(f"Skipping small image: {img_url}")
                return False
            
            img_name = os.path.join(save_folder, img_url.split("/")[-1])
            with open(img_name, 'wb') as handler:
                handler.write(img_data)
            print(f"Image downloaded: {img_name}")

            with open(log_file, 'a') as log:
                log.write(f"Image URL: {img_url} -> Saved as: {img_name}\n")
            
            return True
        except Exception as e:
            print(f"Error downloading image: {e}")
            return False

    def get_image_urls_from_soup(self, url):
        """Extract image URLs from a webpage using BeautifulSoup."""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            img_tags = soup.find_all('img')
            urls = [img['src'] for img in img_tags if 'src' in img.attrs and not img['src'].endswith(('.svg', '.gif'))]
            return urls
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            return []

    def scrape_website_for_images(self, url, save_folder, log_file):
        """Scrape a website for images using Selenium."""
        driver = webdriver.Chrome(service=Service(self.driver_path), options=self.chrome_options)
        driver.get(url)
        scroll_down(driver)

        images = driver.find_elements(By.TAG_NAME, 'img')
        image_urls = [img.get_attribute('src') for img in images if img.get_attribute('src') and not img.get_attribute('src').endswith(('.svg', '.gif'))]

        driver.quit()
        return image_urls

    def scrape_images(self, query, websites, save_folder):
        """Scrape images from multiple websites."""
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        log_file = os.path.join(save_folder, "image_log.txt")
        total_images_downloaded = 0

        for site in websites:
            print(f"Scraping images from: {site}")
            selenium_images = self.scrape_website_for_images(site, save_folder, log_file)
            soup_images = self.get_image_urls_from_soup(site)

            all_images = selenium_images + soup_images
            for img_url in all_images:
                if self.download_image(img_url, save_folder, log_file):
                    total_images_downloaded += 1

        print(f"Total images downloaded: {total_images_downloaded}")
