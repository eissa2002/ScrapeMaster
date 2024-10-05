from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from utils import scroll_down

class YouTubeChannelScraper:
    def __init__(self, driver_path, chrome_options=None):
        """Initialize the channel scraper."""
        self.driver_path = driver_path
        self.chrome_options = chrome_options if chrome_options else Options()

    def scrape_channel_links(self, search_term, desired_channel_count=200, max_scrolls=100):
        """Scrape YouTube channel links based on the search term."""
        print("Initializing WebDriver for channel scraping...")
        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=self.chrome_options)

        # Open YouTube search page with filters for channels
        youtube_search_url = f"https://www.youtube.com/results?search_query={search_term}&sp=EgIQAg%253D%253D"
        driver.get(youtube_search_url)
        time.sleep(5)

        # Store channel links
        channel_links = set()

        # Scroll and scrape channels
        scroll_count = 0
        previous_link_count = 0
        consecutive_no_new_links = 0

        while len(channel_links) < desired_channel_count and scroll_count < max_scrolls and consecutive_no_new_links < 5:
            driver.execute_script("window.scrollBy(0, 3000);")
            time.sleep(5)

            # Get the page source and parse with BeautifulSoup
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, 'lxml')

            # Extract channel links
            for link in soup.find_all('a', class_='channel-link yt-simple-endpoint style-scope ytd-channel-renderer'):
                href = link.get('href')
                if href:
                    full_link = f"https://www.youtube.com{href}"
                    channel_links.add(full_link)

            print(f"Scroll {scroll_count + 1}: Found {len(channel_links)} unique channel links so far.")

            # Check if new links were found
            if len(channel_links) == previous_link_count:
                consecutive_no_new_links += 1
            else:
                consecutive_no_new_links = 0

            previous_link_count = len(channel_links)
            scroll_count += 1

        driver.quit()
        return list(channel_links)

class YouTubeVideoScraper:
    def __init__(self, driver_path, chrome_options=None):
        """Initialize the video scraper."""
        self.driver_path = driver_path
        self.chrome_options = chrome_options if chrome_options else Options()

    def scrape_video_links(self, channel_url, max_videos=50):
        """Scrape video links from a YouTube channel."""
        print(f"Scraping video links from channel: {channel_url}")
        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=self.chrome_options)

        # Open the channel's video page
        video_page_url = f"{channel_url}/videos"
        driver.get(video_page_url)

        # Scroll to load videos
        scroll_down(driver)

        # Get the page source and parse it
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'lxml')

        # Collect video links
        video_links = set()
        for link in soup.find_all('a', id='thumbnail'):
            href = link.get('href')
            if href:
                full_link = f"https://www.youtube.com{href}"
                video_links.add(full_link)

            if len(video_links) >= max_videos:
                break

        print(f"Found {len(video_links)} video links from channel: {channel_url}")
        driver.quit()
        return list(video_links)

    def scrape_videos_from_channels(self, channel_links, max_videos_per_channel=50):
        """Scrape videos from multiple YouTube channels."""
        all_video_links = {}
        for channel_url in channel_links:
            video_links = self.scrape_video_links(channel_url, max_videos_per_channel)
            all_video_links[channel_url] = video_links
        return all_video_links
